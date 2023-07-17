import logging as log
from . import actionstore as action_store
from .clients import get_batch_client, get_core_api_client, get_apps_client


@action_store.kubiya_action()
def health_check():
    apps = get_apps_client()
    batch = get_batch_client()
    core = get_core_api_client()
    return _conn(c=core) and _conn(c=apps) and _conn(c=batch)


def _conn(c) -> bool:
    try:
        return c.get_api_resources().items >= 1
    except Exception as e:
        log.error("[error]", exception=str(e))
        return False
