import time
import threading
from pydantic import BaseModel
from typing import Optional
from . import actionstore as action_store, clients
import logging
import json

# Init logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Deployment(BaseModel):
    deployment_name: Optional[str] = None
    namespace: Optional[str] = "default"

class DeploymentReplicasInput(BaseModel):
    deployment_name: Optional[str] = None
    namespace: Optional[str] = "default"
    replicas: Optional[int] = None

@action_store.kubiya_action()
def get_deployment_logs(params):
    logger.info("Attempting to get logs for deployment " + params["deployment"] + " in namespace " + params["namespace"])
    # Get the deployment
    api_client = clients.get_apps_client()
    logger.info("Reading deployment " + params["deployment"] + " in namespace " + params["namespace"])
    deployment = api_client.read_namespaced_deployment(
        name=params["deployment"],
        namespace=params["namespace"],
    )
    logger.info("Got deployment " + params["deployment"] + " in namespace " + params["namespace"])
    # Get the labels from the deployment
    logger.info("Getting labels from deployment")
    labels = deployment.spec.template.metadata.labels
    label_selector = ",".join([f"{key}={value}" for key, value in labels.items()])
    logger.info("Using label selector " + label_selector)
    # Get the logs for a deployment
    core_api_client = clients.get_core_api_client()
    # Get the pods for the deployment
    api_response = core_api_client.list_namespaced_pod(
        namespace=params["namespace"],
        label_selector=label_selector,
    )
    lines_to_tail = None
    if "lines_to_tail" in params:
        lines_to_tail = int(params["lines_to_tail"])
    else:
        lines_to_tail = 10
    log_lines = []
    if api_response.items:
        for pod in api_response.items:
            # Get the logs for each pod
            # Limit the number of lines to 10 from each pod - from the end of the log
            log_response = core_api_client.read_namespaced_pod_log(
                name=pod.metadata.name,
                namespace=params["namespace"],
                tail_lines=lines_to_tail,
            )
            log_lines.append("[Pod: " + pod.metadata.name + "]\n" + log_response)
            # Combine the logs from all pods into a single string
            output_str = "/n".join(log_lines)
    else:
        output_str = "No pods found for deployment " + params["deployment"]
        logger.info(output_str)
    logger.info("Returning logs for deployment " + params["deployment"])
    return output_str

@action_store.kubiya_action()
def describe_deployment(params):
    api_client = clients.get_apps_client()
    logger.info("Getting deployment " + params["deployment"])
    api_response = api_client.read_namespaced_deployment(
        name=params["deployment"], namespace=params["namespace"]
    )
    # Return the deployment as a JSON string
    logger.info("Returning deployment " + params["deployment"])
    return json.dumps(api_response.to_dict())

@action_store.kubiya_action()
def rollout_restart_deployment(params: Deployment):
    logger.info("Restarting deployment " + params.deployment_name)
    api_client = clients.get_apps_client()

    def patch_deployment():
        nonlocal api_response
        api_response = api_client.patch_namespaced_deployment(
            name=params.deployment_name,
            namespace=params.namespace,
            body={
                "spec": {
                    "template": {"metadata": {"labels": {"date": str(time.time())}}}
                }
            },
        )

    api_response = None
    thread = threading.Thread(target=patch_deployment)
    thread.start()
    thread.join(timeout=10)

    ret = {"status": "success"}
    logger.info("Restarted deployment " + params.deployment_name)
    return ret

@action_store.kubiya_action()
def set_deployment_image(args):
    try:
        logger.info("Setting image for deployment " + args.get("deployment_name"))
        api_client = clients.get_apps_client()
        api_response = api_client.read_namespaced_deployment(args.get("deployment_name"), args.get("namespace"))
        api_response.spec.template.spec.containers[0].image = args.get("image")
        api_response = api_client.patch_namespaced_deployment(args.get("deployment_name"), args.get("namespace"), api_response)
        return api_response.spec.template.spec.containers[0].image
    except api_client.rest.ApiException as e:
        return {"error": e.reason}

@action_store.kubiya_action()
def get_deployment_image(args):
    try:
        logger.info("Getting image for deployment " + args.get("deployment_name"))
        api_client = clients.get_apps_client()
        api_response = api_client.read_namespaced_deployment(args.get("deployment_name"), args.get("namespace"))
        return api_response.spec.template.spec.containers[0].image
    except api_client.rest.ApiException as e:
        logger.error(e.reason)
        return {"error": e.reason}
    
@action_store.kubiya_action()
def get_deployment_replicas(args):
    try:
        logger.info("Getting replicas for deployment " + args.get("deployment_name"))
        api_client = clients.get_apps_client()
        api_response = api_client.read_namespaced_deployment(args.get("deployment_name"), args.get("namespace"))
        logger.info("Replicas for deployment " + args.get("deployment_name") + " is " + str(api_response.spec.replicas))
        return api_response.spec.replicas
    except api_client.rest.ApiException as e:
        logger.error(e.reason)
        return {"error": e.reason}
    
@action_store.kubiya_action()
def set_deployment_replicas(args: DeploymentReplicasInput):
    try:
        api_client = clients.get_apps_client()
        api_response = api_client.read_namespaced_deployment(args.get("deployment_name"), args.get("namespace"))
        api_response.spec.replicas = args.get("replicas")
        api_response = api_client.patch_namespaced_deployment(args.get("deployment_name"), args.get("namespace"), api_response)
        return api_response.spec.replicas
    except api_client.rest.ApiException as e:
        logger.error(e.reason)
        return {"error": e.reason}

@action_store.kubiya_action()
def list_deployment(params: Deployment):
    logger.info("Listing deployments")
    api_client = clients.get_apps_client()
    api_response = api_client.list_namespaced_deployment(params.namespace)
    logger.info("Returning deployments")
    return [item.metadata.name for item in api_response.items]
