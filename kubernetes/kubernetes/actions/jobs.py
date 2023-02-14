import datetime
import logging

from datetime import timedelta
from typing import Any, Dict, Optional
from lightkube.resources.core_v1 import Pod
from lightkube.resources import batch_v1 
import requests
from pydantic import BaseModel

import kubernetes
from kubernetes import client, config
from kubernetes.client import (V1Container, V1EnvVar, V1Job, V1JobSpec,
                               V1ObjectMeta, V1PodSpec, V1PodTemplateSpec)
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream

from . import actionstore as action_store
from .clients import get_batch_client, get_lightkube_client

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
    backoff_limit: int = 4


@action_store.kubiya_action()
def create_namespaced_job(job: Job):
    start_time = datetime.datetime.now()
    timeout_time = start_time + timedelta(seconds=job.kubernetes_client_timeout)
    api_client = get_batch_client()

    logging.info("Attempting to create namespaced job")
    if not job.env_vars:
        job.env_vars = {"EXAMPLE_ENV_VAR": "example-value"}
    
    cmd = job.command
    if cmd:
        cmd = [part.strip() for part in job.command.split(",")]
    logging.info("cmd is {}".format(cmd))

    container = V1Container(
        name=job.container_name,
        image=job.image,
        command=cmd,
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
        backoff_limit=job.backoff_limit,
    )

    # Create the job
    new_job = V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=V1ObjectMeta(name=job.job_name),
        spec=job_spec,
    )
    try:
        ret = api_client.create_namespaced_job(
            namespace=job.namespace, body=new_job
        )
        return ret.to_dict()
        
    except ApiException as e:
        # create a meaningful error message
        raise ApiException(
            f"Exception when calling BatchV1Api->create_namespaced_job: {e.body}"
        )
        # In case the job succeeded to start, get its logs
   
        raise ApiException(
            f"Exception when calling BatchV1Api->read_namespaced_job: {e.body}"
        )

@action_store.kubiya_action()
def get_pods(job: Job):
    try:
        client = get_lightkube_client()
        return [
            pod.to_dict()
            for pod in client.list(Pod, namespace=job.namespace, labels={"job-name": job.name})
        ]
    except ApiException as e:
        raise ApiException(
            e.msg
        )

@action_store.kubiya_action()
def get_job_data(job: Job):
    try:
        client = get_lightkube_client()
        return client.list(batch_v1.Job, name=job.name, namespace=job.namespace).to_dict()
    except ApiException as e:
        raise ApiException(
            e.msg
        )
    
@action_store.kubiya_action()
def get_job_per_pod_status(job: Job):
    try:
        client = get_lightkube_client()
        return [
            pod.status.phase
            for pod in client.list(Pod, namespace=job.namespace, labels={"job-name": job.name})
        ]
    except ApiException as e:
        raise ApiException(
            e.msg
        )

@action_store.kubiya_action()
def list_job_names(job: Job):
    try:
        client = get_lightkube_client()
        return [
            job.metadata.name
            for job in client.list(
                batch_v1.Job, namespace=job.namespace
            )
        ]
    except ApiException as e:
        raise ApiException(
            e.msg
        )
   
@action_store.kubiya_action()
def get_job_status(job: Job):
    client = get_lightkube_client()
    return client.get(batch_v1.Job, name=job.name, namespace=job.namespace).status.conditions[-1].type

@action_store.kubiya_action()
def list_job_statuses(job: Job):
    try:
        client = get_lightkube_client()
        return {
        job.metadata.name: job.status.conditions[-1].type
        for job in client.list(batch_v1.Job, namespace=job.namespace)
    }
    except ApiException as e:
        raise ApiException(
            e.msg
        )
        
@action_store.kubiya_action()
def delete_job(job: Job):
    try:
        client = get_lightkube_client()
        client.delete(
            batch_v1.Job, name=job.name, namespace=job.namespace
        )
        return True
    except ApiException as e:
        raise ApiException(
            e.msg
        )
    
@action_store.kubiya_action()
def get_job_logs(job: Job):
    try:
        client = get_lightkube_client()
        podnames = [
            pod.metadata.name
            for pod in client.list(Pod, namespace=job.namespace, labels={"job-name": job.name})
        ]
        if len(podnames) == 0:
            return {"status": "No pods found"}
        return {
            podname: "".join(client.log(name=podname, namespace=job.namespace))
            for podname in podnames
        }
    except ApiException as e:
        raise ApiException(
            e.msg
        )