from typing import Optional

from pydantic import BaseModel

from kubernetes import client

from . import actionstore as action_store


class NamespacedPod(BaseModel):
    """follows model with attributes of namespaced pod for kubernetes"""

    pod_name: str
    namespace: Optional[str] = None


@action_store.kubiya_action()
def create_namespaced_pod(namespaced_pod: NamespacedPod):
    """creates a namespaced pod"""
    try:
        core_api = client.CoreV1Api()
        pod = kubernetes.client.V1Pod(
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
        core_api = client.CoreV1Api()
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
        core_api = client.CoreV1Api()
        res = core_api.list_namespaced_pod(namespace=namespaced_pod.namespace)
        return {"data": [pod.to_dict() for pod in res.items]}
    except client.rest.ApiException as e:
        return {"error": e.reason}


@action_store.kubiya_action()
def patch_namespaced_pod(namespaced_pod: NamespacedPod):
    """patches a namespaced pod"""
    try:
        core_api = client.CoreV1Api()
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
        core_api = client.CoreV1Api()
        res = core_api.read_namespaced_pod(
            name=namespaced_pod.pod_name, namespace=namespaced_pod.namespace
        )
        return {"data": res.to_dict()}
    except client.rest.ApiException as e:
        return {"error": e.reason}
