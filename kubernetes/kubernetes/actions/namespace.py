from . import actionstore as action_store
from .clients import get_batch_client, get_core_api_client

@action_store.kubiya_action()
def list_namespace(params):
    api_client = get_core_api_client()
    api_response = api_client.list_namespace()
    return [item.metadata.name for item in api_response.items]