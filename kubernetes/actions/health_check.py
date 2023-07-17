import logging as log
from typing import List

from pydantic import BaseModel
from . import actionstore as action_store
from .clients import get_batch_client, get_core_api_client, get_apps_client

class HealthRequest(BaseModel):
    pass

class HealthResponse(BaseModel):
    params: bool
    connection: bool
    errors: List[str]


@action_store.kubiya_action()
def health_check(_) -> HealthResponse:
    errs = []
    apps = get_apps_client()
    batch = get_batch_client()
    core = get_core_api_client()
    valid_core = _conn(c=core, e=errs)
    valid_apps = _conn(c=apps, e=errs)
    valid_batch = _conn(c=batch, e=errs)
    
    valid_conn = valid_core and valid_apps and valid_batch
    return HealthResponse(params=True, connection=valid_conn , errors=errs)


def _conn(c, e: List[str]) -> bool:
    try:
        return c.get_api_resources().items >= 1
    except Exception as e:
        log.error("[error]", exception=str(e))
        return False
