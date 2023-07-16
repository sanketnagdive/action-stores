import logging as log
from .clients import get_batch_client, get_core_api_client, get_apps_client

def health_check():
    apps = get_apps_client()
    batch = get_batch_client()
    core = get_core_api_client()
    return _conn(c=core) & _conn(c=apps) & _conn(c=batch)


def _conn(c) -> bool:
    try:
        return c.get_api_resources().items >= 1
    except Exception as e:
        log.error("[error]", exception=str(e))
        return False
