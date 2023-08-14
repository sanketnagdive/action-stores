import time
import threading
from pydantic import BaseModel
from typing import Optional, Dict, Any, List , Literal
from . import actionstore as action_store, clients ,NameSpacesforPlayground
from .utils import convert_datetime
from kubernetes import client
import logging
import json

# Init logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ListDeploymentsInput(BaseModel):
    namespace: NameSpacesforPlayground

class Deployment(BaseModel):
    deployment_name: Optional[str] = None
    namespace: NameSpacesforPlayground

class DeploymentReplicasInput(BaseModel):
    deployment_name: Optional[str] = None
    namespace: NameSpacesforPlayground
    replicas: Optional[int] = None

class DeploymentReplicasInputSingle(BaseModel):
    deployment_name: Optional[str] = None
    replicas: Optional[int] = None

class DeploymentsReplicasInput(BaseModel):
    namespace: NameSpacesforPlayground
    inputs: List[DeploymentReplicasInputSingle]


class DeploymentImageInput(BaseModel):
    deployment_name: Optional[str] = None
    namespace: NameSpacesforPlayground
    image: Optional[str] = None

# # For playground - limit to default namespace
# NamespaceType=Literal["default"]
class DeploymentBodyInput(BaseModel):
    deployment_name: Optional[str] = None
    namespace: NameSpacesforPlayground
    body: Dict[str, Any] = {}

class DeploymentStatusInput(BaseModel):
    deployment_name: str
    namespace: NameSpacesforPlayground

class DeploymentStatus(BaseModel):
    available_replicas: int
    updated_replicas: int
    ready_replicas: int

class RollbackDeploymentInput(BaseModel):
    deployment_name: str
    namespace: NameSpacesforPlayground

class DeploymentLogsInput(BaseModel):
    deployment: str
    namespace: NameSpacesforPlayground
    lines_to_tail: Optional[int] = 10

class PodLogs(BaseModel):
    pod_name: str
    logs: str

class DeploymentUpdate(BaseModel):
    deployment_name: str
    namespace: NameSpacesforPlayground
    image: Optional[str] = None
    replicas: Optional[int] = None

class DeploymentInfo(BaseModel):
    namespace: NameSpacesforPlayground
    deployment_name: str



@action_store.kubiya_action()
def describe_deployment(deployment_info: DeploymentInfo):
    try:
        apps_api = clients.get_apps_client()
        api_response = apps_api.read_namespaced_deployment(
            name=deployment_info.deployment_name,
            namespace=deployment_info.namespace
        )

        # Convert V1Deployment to dictionary
        deployment_dict = api_response.to_dict()

        # Convert datetime objects to strings
        deployment_dict = convert_datetime(deployment_dict)

        # Return the deployment as a JSON string
        return json.dumps(deployment_dict)
    except client.rest.ApiException as e:
        return {"error": e.reason}

# @action_store.kubiya_action()
def update_deployment(deployment_update: DeploymentUpdate):

    try:
        apps_api = clients.get_apps_client()
        deployment = apps_api.read_namespaced_deployment(
            name=deployment_update.deployment_name,
            namespace=deployment_update.namespace
        )

        # Update the deployment
        if deployment_update.image:
            deployment.spec.template.spec.containers[0].image = deployment_update.image

        if deployment_update.replicas is not None:
            deployment.spec.replicas = deployment_update.replicas

        updated_deployment = apps_api.patch_namespaced_deployment(
            name=deployment_update.deployment_name,
            namespace=deployment_update.namespace,
            body=deployment
        )

        return {"data": updated_deployment.to_dict()}
    except client.rest.ApiException as e:
        return {"error": e.reason}

@action_store.kubiya_action()
def get_deployment_logs(input_data: DeploymentLogsInput) -> List[PodLogs]:

    try:
        apps_v1_api = clients.get_apps_client()
        core_v1_api = clients.get_core_api_client()

        deployment = apps_v1_api.read_namespaced_deployment(
            name=input_data.deployment,
            namespace=input_data.namespace,
        )

        labels = deployment.spec.template.metadata.labels
        label_selector = ",".join([f"{key}={value}" for key, value in labels.items()])

        pods = core_v1_api.list_namespaced_pod(
            namespace=input_data.namespace,
            label_selector=label_selector,
        ).items

        logs = []
        for pod in pods:
            log_response = core_v1_api.read_namespaced_pod_log(
                name=pod.metadata.name,
                namespace=input_data.namespace,
                tail_lines=input_data.lines_to_tail,
            )
            logs.append(PodLogs(pod_name=pod.metadata.name, logs=log_response))

        return logs

    except client.rest.ApiException as e:
        return {"error": e.reason}

@action_store.kubiya_action()
def rollback_deployment(input_data: RollbackDeploymentInput):

    try:
        apps_v1_api = clients.get_apps_client()
        rollback_options = client.V1RollbackConfig(
            kind="Deployment",
            name=input_data.deployment_name,
            rollback_to=client.V1RollbackConfigRollbackTo(
                revision=0  # Set the desired revision number to rollback to
            ),
        )
        api_response = apps_v1_api.create_namespaced_deployment_rollback(
            namespace=input_data.namespace,
            name=input_data.deployment_name,
            body=rollback_options,
        )
        return {"data": api_response.to_dict()}
    except client.rest.ApiException as e:
        return {"error": e.reason}
    
@action_store.kubiya_action()
def get_deployment_status(input: DeploymentStatusInput) -> DeploymentStatus:
    api_client = clients.get_apps_client()
    api_response = api_client.read_namespaced_deployment_status(
        name=input.deployment_name,
        namespace=input.namespace,
    )
    return DeploymentStatus(
        available_replicas=api_response.status.available_replicas,
        updated_replicas=api_response.status.updated_replicas,
        ready_replicas=api_response.status.ready_replicas,
    )

@action_store.kubiya_action()
def rollout_status(deployment_info: Deployment):
    """ Check the rollout status of a deployment """
    apps_api = clients.get_apps_client()
    deployment_status = apps_api.read_namespaced_deployment_status(
        name=deployment_info.deployment_name,
        namespace=deployment_info.namespace,
    )

    if deployment_status.spec.replicas != deployment_status.status.replicas:
        return {
            "status": "Rollout in progress",
            "details": {
                "desired_replicas": deployment_status.spec.replicas,
                "current_replicas": deployment_status.status.replicas,
            },
        }

    elif deployment_status.status.available_replicas != deployment_status.status.replicas:
        return {
            "status": "Rollout in progress",
            "details": {
                "desired_available_replicas": deployment_status.spec.replicas,
                "current_available_replicas": deployment_status.status.available_replicas,
            },
        }

    elif deployment_status.metadata.generation != deployment_status.status.observed_generation:
        return {
            "status": "Rollout in progress",
            "details": {
                "observed_generation": deployment_status.status.observed_generation,
                "current_generation": deployment_status.metadata.generation,
            },
        }
    
    return {
        "status": "Rollout complete",
        "details": {
            "desired_replicas": deployment_status.spec.replicas,
            "current_replicas": deployment_status.status.replicas,
            "desired_available_replicas": deployment_status.spec.replicas,
            "current_available_replicas": deployment_status.status.available_replicas,
            "observed_generation": deployment_status.status.observed_generation,
            "current_generation": deployment_status.metadata.generation,
        },
    }


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

# @action_store.kubiya_action()
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
def get_deployment_image(args:Deployment):
    try:
        logger.info("Getting image for deployment " + args.deployment_name)
        api_client = clients.get_apps_client()
        api_response = api_client.read_namespaced_deployment(args.deployment_name, args.namespace)
        return api_response.spec.template.spec.containers[0].image
    except api_client.rest.ApiException as e:
        logger.error(e.reason)
        return {"error": e.reason}
    
@action_store.kubiya_action()
def get_deployment_replicas(args:Deployment):
    try:
        logger.info("Getting replicas for deployment " + args.deployment_name)
        api_client = clients.get_apps_client()
        api_response = api_client.read_namespaced_deployment(args.deployment_name, args.namespace)
        logger.info("Replicas for deployment " + args.deployment_name + " is " + str(api_response.spec.replicas))
        return api_response.spec.replicas
    except api_client.rest.ApiException as e:
        logger.error(e.reason)
        return {"error": e.reason}
    
@action_store.kubiya_action()
def set_deployment_replicas(args: DeploymentReplicasInput):
    try:
        api_client = clients.get_apps_client()
        api_response = api_client.read_namespaced_deployment(args.deployment_name, args.namespace)
        api_response.spec.replicas = args.replicas
        api_response = api_client.patch_namespaced_deployment(args.deployment_name, args.namespace, api_response)
        return api_response.spec.replicas
    except api_client.rest.ApiException as e:
        logger.error(e.reason)
        return {"error": e.reason}

@action_store.kubiya_action()
def list_deployment(params: ListDeploymentsInput):
    logger.info("Listing deployments")
    api_client = clients.get_apps_client()
    api_response = api_client.list_namespaced_deployment(params.namespace)
    logger.info("Returning deployments")
    return [item.metadata.name for item in api_response.items]

@action_store.kubiya_action()
def scale_deployment(params: DeploymentReplicasInput):
    try:
        logger.info(f"Scaling deployment {params.deployment_name} to {params.replicas} replicas")
        api_client = clients.get_apps_client()
        deployment = api_client.read_namespaced_deployment(params.deployment_name, params.namespace)
        deployment.spec.replicas = params.replicas
        api_response = api_client.patch_namespaced_deployment(params.deployment_name, params.namespace, deployment)
        return {"status": "success", "replicas": api_response.spec.replicas}
    except api_client.rest.ApiException as e:
        logger.error(e.reason)
        return {"error": e.reason}

@action_store.kubiya_action()
def scale_deployments(params: DeploymentsReplicasInput):
    # if params.namespace in EXCLUDED_NAMESPACES:
    #     return {"error": f"Namespace {params.namespace} is excluded from this action"}
    logger.info(f"Scaling {len(params.inputs)} deployments")
    res_dict = {}
    for i, _input in enumerate(params.inputs):
        logger.info(f"Scaling deployment {i+1}/{len(params.inputs)}...")
        scale_input = DeploymentReplicasInput(
            deployment_name=_input.deployment_name,
            namespace=params.namespace,
            replicas=_input.replicas,
        )
        res = scale_deployment(scale_input)
        res_dict[_input.deployment_name] = res

    success = []
    failed = []
    for deployment_name, res in res_dict.items():
        e = res.get("error")
        if e is not None:
            failed.append({"deployment": deployment_name, "namespace": params.namespace, "error": e})
        else:
            success.append({"deployment": deployment_name, "namespace": params.namespace})

    logger.info(f"Finished scaling deployments")
    if failed:
        return {"success": success, "failed": failed, "error": failed}
    return {"success": success, "failed": failed}

# @action_store.kubiya_action()
def delete_deployment(params: Deployment):
    try:
        logger.info(f"Deleting deployment {params.deployment_name}")
        api_client = clients.get_apps_client()
        api_response = api_client.delete_namespaced_deployment(params.deployment_name, params.namespace)
        return {"status": "success"}
    except api_client.rest.ApiException as e:
        logger.error(e.reason)
        return {"error": e.reason}

@action_store.kubiya_action()
def check_deployment_status(params: Deployment):
    try:
        logger.info(f"Checking deployment status for {params.deployment_name}")
        api_client = clients.get_apps_client()
        deployment = api_client.read_namespaced_deployment_status(params.deployment_name, params.namespace)
        return {"status": deployment.status}
    except api_client.rest.ApiException as e:
        logger.error(e.reason)
        return {"error": e.reason}

# @action_store.kubiya_action()
def create_deployment(params: DeploymentBodyInput):
    try:
        logger.info(f"Creating deployment {params.deployment_name}")
        api_client = clients.get_apps_client()
        deployment = api_client.create_namespaced_deployment(params.namespace, params.body)
        return {"status": "success", "deployment": deployment.to_dict()}
    except api_client.rest.ApiException as e:
        logger.error(e.reason)
        return {"error": e.reason}
