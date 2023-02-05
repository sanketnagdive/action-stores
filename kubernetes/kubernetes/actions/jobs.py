import datetime
import logging
import os
import time
from datetime import timedelta
from typing import Any, Dict, Optional, Union

import requests
from pydantic import BaseModel

import kubernetes
from kubernetes import client, config
from kubernetes.client import (V1Container, V1EnvVar, V1Job, V1JobSpec,
                               V1ObjectMeta, V1PodSpec, V1PodTemplateSpec)
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream

from . import actionstore as action_store
from .clients import get_batch_client, get_core_api_client

logging.basicConfig(level=logging.INFO)


class Job(BaseModel):
    name: str
    image: str
    command: Optional[str]
    resources: Optional[dict] = None
    kubernetes_client_retry_attempts: int = 44
    kubernetes_client_timeout: int = 55
    job_name: str = "example-job"
    namespace: str = "openfaas-fn"
    image: str = "nginx:latest"
    container_name: str = "example-container"
    env_vars: Optional[Dict[str, str]] = None
    app_label: str = "example-app"
    restart_policy: str = "Never"


@action_store.kubiya_action()
def create_namespaced_job(job: Job):
    start_time = datetime.datetime.now()
    timeout_time = start_time + timedelta(seconds=job.kubernetes_client_timeout)
    api_client = get_batch_client()

    logging.info("Attempting to create namespaced job")
    if not job.env_vars:
        job.env_vars = {"EXAMPLE_ENV_VAR": "example-value"}
    container = V1Container(
        name=job.container_name,
        image=job.image,
        env=[V1EnvVar(name=k, value=v) for k, v in job.env_vars.items()],
    )

    # Create the specification of deployment
    # Restart policy is set to Never, so that the pod will not be restarted in case of failure
    job_spec = V1JobSpec(
        template=V1PodTemplateSpec(
            metadata=V1ObjectMeta(labels={"app": job.app_label}),
            spec=V1PodSpec(
                containers=[container],
                # TODO:: Support ability to pass dynamic commands
                restart_policy=job.restart_policy,
            ),
        ),
        backoff_limit=4,
    )

    # Create the job
    new_job = V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=V1ObjectMeta(name=job.job_name),
        spec=job_spec,
    )
    try:
        api_response = api_client.create_namespaced_job(
            namespace=job.namespace, body=new_job
        )
        logging.info(f"Job created. response='{str(api_response)}")
    except ApiException as e:
        # create a meaningful error message
        raise ApiException(
            f"Exception when calling BatchV1Api->create_namespaced_job: {e.body}"
        )
        # In case the job succeeded to start, get its logs
    try:
        # Wait for the job to launch a pod
        while datetime.datetime.now() < timeout_time:
            logging.info("Waiting for job to start")
            api_response = api_client.read_namespaced_job(job.job_name, job.namespace)
            # Get the pod name from the job
            logging.info(f"current status: {api_response}")

            if api_response.status.active not in [None, 0]:
                return {"status": api_response.status.active}
            time.sleep(1.5)

    except ApiException as e:
        raise ApiException(
            f"Exception when calling BatchV1Api->read_namespaced_job: {e.body}"
        )


@action_store.kubiya_action()
def get_namespaced_job_logs(job: Job):
    try:
        core_api_client = get_core_api_client()

        label_selector = f"job-name={job.job_name}"
        pod_list = core_api_client.list_namespaced_pod(
            job.namespace, label_selector=label_selector
        )
        pod_name = pod_list.items[0].metadata.name
        logging.info(f"Found pod:{pod_name}")

        while True:
            pod = core_api_client.read_namespaced_pod(pod_name, job.namespace)
            if pod.status.phase != "Pending":
                logs = core_api_client.read_namespaced_pod_log(pod_name, job.namespace)
                return logs.splitlines()
            time.sleep(1)
    except Exception as e:
        raise Exception(
            f"Exception when calling BatchV1Api->create_namespaced_job: {e}"
        )
