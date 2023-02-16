from typing import Optional

from pydantic import BaseModel

from kubernetes import client


from . import actionstore as action_store, clients


class NamespacedPod(BaseModel):
    """follows model with attributes of namespaced pod for kubernetes"""

    pod_name: str
    namespace: Optional[str] = None

class Pod(BaseModel):
    """follows model with attributes of pod for kubernetes"""

    pod_name: str
    namespace: Optional[str] = None


@action_store.kubiya_action()
def create_namespaced_pod(namespaced_pod: NamespacedPod):
    """creates a namespaced pod"""
    try:
        core_api = clients.get_core_api_client()
        pod = client.V1Pod(
            api_version="v1",
            kind="Pod",
            metadata=client.V1ObjectMeta(name=namespaced_pod.pod_name),
        )
        res = core_api.create_namespaced_pod(
            namespace=namespaced_pod.namespace, body=pod
        )
        return {"data": res.to_dict()}
    except client.rest.ApiException as e:
        return {"error": e.reason}

@action_store.kubiya_action()
def delete_namespaced_pod(namespaced_pod: NamespacedPod):
    """deletes a namespaced pod"""
    try:
        core_api = clients.get_core_api_client()
        res = core_api.delete_namespaced_pod(
            name=namespaced_pod.pod_name,
            namespace=namespaced_pod.namespace,
            body=client.V1DeleteOptions(),
        )
        return {"data": res.to_dict()}
    except client.rest.ApiException as e:
        return {"error": e.reason}


@action_store.kubiya_action()
def list_namespaced_pod(namespaced_pod: NamespacedPod):
    """lists all namespaced pods"""
    try:
        core_api = clients.get_core_api_client()
        res = core_api.list_namespaced_pod(namespace=namespaced_pod.namespace, FieldSelector=field_selector)
        return {"data": [pod.to_dict() for pod in res.items]}
    except client.rest.ApiException as e:
        return {"error": e.reason}


@action_store.kubiya_action()
def patch_namespaced_pod(namespaced_pod: NamespacedPod):
    """patches a namespaced pod"""
    try:
        core_api = clients.get_core_api_client()
        res = core_api.patch_namespaced_pod(
            name=namespaced_pod.pod_name, namespace=namespaced_pod.namespace, body={}
        )
        return {"data": res.to_dict()}
    except client.rest.ApiException as e:
        return {"error": e.reason}


@action_store.kubiya_action()
def read_namespaced_pod(namespaced_pod: NamespacedPod):
    """reads a namespaced pod"""
    try:
        core_api = clients.get_core_api_client()
        res = core_api.read_namespaced_pod(
            name=namespaced_pod.pod_name, namespace=namespaced_pod.namespace
        )
        return {"data": res.to_dict()}
    except client.rest.ApiException as e:
        return {"error": e.reason}

@action_store.kubiya_action()
def list_failed_pods(params):
    """ "Kubernetes AS - Show logs for a pod that is in degraded state"""
    api_client = clients.get_core_api_client()
    field_selector = "status.phase=Failed"
    api_response = api_client.list_pod_for_all_namespaces(field_selector=field_selector)
    return [item.metadata.name for item in api_response.items]


@action_store.kubiya_action()
def list_pods(params):
    """Kubernetes AS - List pods"""
    if params.get("namespace"):
        api_client = clients.get_core_api_client()
        api_response = api_client.list_namespaced_pod(params.get("namespace"))
        return [item.metadata.name for item in api_response.items]
    else:
        api_client = clients.get_core_api_client()
        api_response = api_client.list_pod_for_all_namespaces()
        return [item.metadata.name for item in api_response.items]


@action_store.kubiya_action()
def retreive_image_tag_for_pod(input_pod: Pod):
    try:
        api_client = clients.get_core_api_client()
        api_response = api_client.list_pod_for_all_namespaces(
            field_selector="status.phase=Running"
        )

        pod = [
            item
            for item in api_response.items
            if item.metadata.name == input_pod.pod_name
        ]
        if not pod:
            return {"response": "Pod not found"}
        return pod[0].spec.containers[0].image.split(":")[1]
    except client.rest.ApiException as e:
        return {"error": e.reason}

@action_store.kubiya_action()
def get_pods(args):
    try:
        field_selector = "status.phase=Running"
        api_client = clients.get_core_api_client()
        if args.get("field_selector"):
            field_selector = args.get("field_selector")
        if args.get("namespace"):
            api_response = api_client.list_namespaced_pod(args.get("namespace"), field_selector=field_selector)
            return [item.metadata.name for item in api_response.items]
        else:
            api_response = api_client.list_pod_for_all_namespaces(field_selector=field_selector)
            return [item.metadata.name for item in api_response.items]
    except client.rest.ApiException as e:
        return {"error": e.reason}

@action_store.kubiya_action()
def get_pods_with_degraded_status(args):
    try:
        field_selector = "status.phase=Failed"
        api_client = clients.get_core_api_client()
        if args.get("field_selector"):
            field_selector = args.get("field_selector")
        if args.get("namespace"):
            api_response = api_client.list_namespaced_pod(args.get("namespace"), field_selector=field_selector)
            return [item.metadata.name for item in api_response.items]
        else:
            api_response = api_client.list_pod_for_all_namespaces(field_selector=field_selector)
            return [item.metadata.name for item in api_response.items]
    except client.rest.ApiException as e:
        return {"error": e.reason}

@action_store.kubiya_action()
def get_logs_for_pod(args):
    try:
        api_client = clients.get_core_api_client()
        if args.get("namespace"):
            api_response = api_client.read_namespaced_pod_log(args.get("pod_name"), args.get("namespace"))
            return api_response
        else:
            # limit the number of lines to 10
            # get the logs for a pod in all namespaces
            api_response = api_client.read_namespaced_pod_log(args.get("pod_name"), "default", tail_lines=10)
            return api_response
    except client.rest.ApiException as e:
        return {"error": e.reason}

@action_store.kubiya_action()
def get_running_pods(args):
    try:
        api_client = clients.get_core_api_client()
        if args.get("namespace"):
            api_response = api_client.list_namespaced_pod(args.get("namespace"), field_selector="status.phase=Running")
            return [item.metadata.name for item in api_response.items]
        else:
            api_response = api_client.list_pod_for_all_namespaces(field_selector="status.phase=Running")
            return [item.metadata.name for item in api_response.items]
    except client.rest.ApiException as e:
        return {"error": e.reason}

class PodMeta(BaseModel):
    namespace: str 
    label: str

@action_store.kubiya_action()
def get_pod_logs_by_label(args: PodMeta):
    api_client = clients.get_core_api_client()
    label_selector = "controller-uid={}".format(args.label)
    api_response = api_client.list_namespaced_pod(args.namespace, label_selector=label_selector)
    
    
    if api_response.items:
        pod_name = api_response.items[0].metadata.name
        return api_client.read_namespaced_pod_log(pod_name, args.namespace).split("\n")
    else:
        return "No pods found"
