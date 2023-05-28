from . import actionstore as action_store
from .clients import get_batch_client, get_core_api_client
from kubernetes.client import V1Namespace

from pydantic import BaseModel

class NamespaceMeta(BaseModel):
    namespace: str

@action_store.kubiya_action()
# Every action should recieve a param object
def list_namespace(params):
    api_client = get_core_api_client()
    api_response = api_client.list_namespace()
    return [item.metadata.name for item in api_response.items]

@action_store.kubiya_action()
def create_namespace(namespace: NamespaceMeta):
    api_client = get_core_api_client()
    namespace_body = V1Namespace(
        metadata={
            "name": namespace.namespace,
        }
    )
    api_response = api_client.create_namespace(body=namespace_body)
    return {"status": "created", "namespace": api_response.metadata.name}

@action_store.kubiya_action()
def delete_namespace(namespace: NamespaceMeta):
    api_client = get_core_api_client()
    api_response = api_client.delete_namespace(name=namespace.namespace)
    return {"status": "deleted", "namespace": namespace.namespace}

@action_store.kubiya_action()
def get_namespace(namespace: NamespaceMeta):
    api_client = get_core_api_client()
    api_response = api_client.read_namespace(name=namespace.namespace)
    return api_response.to_dict()