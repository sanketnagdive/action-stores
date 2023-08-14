from typing import Optional, List
from kubernetes import client, stream
from pydantic import BaseModel

from . import actionstore as action_store ,NameSpacesforPlayground,EXCLUDED_NAMESPACES
from .clients import get_core_api_client


class NamespacePodPatchModel(BaseModel):
    namespace: str
    pod_name: str
    body: dict

class NamespacePodCreateModel(BaseModel):
    namespace: str
    body: dict
class NamespacePodModel(BaseModel):
    namespace: NameSpacesforPlayground
    pod_name: str
class NamespaceModel(BaseModel):
    namespace: NameSpacesforPlayground


class CommandModel(BaseModel):
    namespace: str
    pod_name: str
    command: List[str]


class DeletePodModel(BaseModel):
    namespace: NameSpacesforPlayground
    pod_name: str


class LabelModel(BaseModel):
    namespace: NameSpacesforPlayground
    label_key: str
    label_value: str

class PodLogsModel(BaseModel):
    logs: List[str]

# Remove this from playgroud
# @action_store.kubiya_action()
def exec_command_in_pod(data: CommandModel) -> str:
    try:
        api_client = get_core_api_client()

        resp = stream.stream(
            api_client.connect_get_namespaced_pod_exec,
            name=data.pod_name,
            namespace=data.namespace,
            command=data.command,
            stderr=True, stdin=True, stdout=True, tty=False
        )

        return resp
    except client.rest.ApiException as e:
        return {"error": e.reason}


@action_store.kubiya_action()
def delete_namespaced_pod(data: DeletePodModel) -> dict:

    try:
        api_client = get_core_api_client()

        resp = api_client.delete_namespaced_pod(
            name=data.pod_name,
            namespace=data.namespace,
            body=client.V1DeleteOptions(),
        )

        return resp.to_dict()
    except client.rest.ApiException as e:
        return {"error": e.reason}


@action_store.kubiya_action()
def list_namespaced_pod(data: NamespaceModel) -> List[dict]:
    try:
        api_client = get_core_api_client()

        resp = api_client.list_namespaced_pod(namespace=data.namespace)

        return [i.to_dict() for i in resp.items]
    except client.rest.ApiException as e:
        return {"error": e.reason}


@action_store.kubiya_action()
def get_pod_logs_by_label(data: LabelModel) -> PodLogsModel:
    try:
        api_client = get_core_api_client()

        # label_selector = "controller-uid={}".format(data.label)
        label_selector = "{}={}".format(data.label_key,data.label_value)
        resp = api_client.list_namespaced_pod(
            namespace=data.namespace, 
            label_selector=label_selector
        )

        if resp.items:
            pod_name = resp.items[0].metadata.name
            pod_logs= api_client.read_namespaced_pod_log(pod_name, data.namespace).split("\n")
            return PodLogsModel(logs=pod_logs)
        else:
            return ["No pods found"]
    except client.rest.ApiException as e:
        return {"error": e.reason}


# @action_store.kubiya_action()
def create_namespaced_pod(data: NamespacePodCreateModel) -> dict:
    # if data.namespace in EXCLUDED_NAMESPACES:
    #     return {"error": "create of this namespace is not allowed"}
    try:
        api_client = get_core_api_client()

        # # Define the pod's container spec
        # container_spec = {
        #     "name": "my-container",
        #     "image": "nginx:latest",  # Use any desired image
        #     "ports": [{"containerPort": 80}]  # Example port configuration
        # }
        #
        # # Define the complete pod specification
        # pod = {
        #     "apiVersion": "v1",
        #     "kind": "Pod",
        #     "metadata": {
        #         "name": "example-pod"
        #     },
        #     "spec": {
        #         "containers": [container_spec]
        #     }
        # }


        resp = api_client.create_namespaced_pod(
            namespace=data.namespace, body=data.body
        )

        return resp.to_dict()
    except client.rest.ApiException as e:
        return {"error": e.reason}


# @action_store.kubiya_action()
def patch_namespaced_pod(data: NamespacePodPatchModel) -> dict:
    # if data.namespace in EXCLUDED_NAMESPACES:
    #     return {"error": "patch of this namespace is not allowed"}
    try:
        api_client = get_core_api_client()

        resp = api_client.patch_namespaced_pod(
            name=data.pod_name,
            namespace=data.namespace, 
            body=data.body
        )

        return resp.to_dict()
    except client.rest.ApiException as e:
        return {"error": e.reason}


@action_store.kubiya_action()
def read_namespaced_pod(data: NamespacePodModel) -> dict:
    try:
        api_client = get_core_api_client()

        resp = api_client.read_namespaced_pod(
            name=data.pod_name,
            namespace=data.namespace
        )

        return resp.to_dict()
    except client.rest.ApiException as e:
        return {"error": e.reason}


@action_store.kubiya_action()
def list_failed_pods(data) -> List[str]:

    try:
        api_client = get_core_api_client()

        field_selector = "status.phase=Failed"
        resp = api_client.list_pod_for_all_namespaces(
            field_selector=field_selector
        )

        return [item.metadata.name for item in resp.items]
    except client.rest.ApiException as e:
        return {"error": e.reason}