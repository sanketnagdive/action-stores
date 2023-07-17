import logging as log
from typing import List

from pydantic import BaseModel
from . import action_store
from .secrets import get_secrets
from .plugins import list_jenkins_plugins

class HealthRequest(BaseModel):
    pass

class HealthResponse(BaseModel):
    params: bool
    connection: bool
    errors: List[str]

@action_store.kubiya_action()
def health_check(_) -> HealthResponse:
    errs = []
    url, user, pwd = get_secrets()
    valid_url = _param(url)
    valid_pwd = _param(pwd)
    valid_user = _param(user)
    
    if not valid_url:
        errs.append("JENKINS_URL is not set")
        
    if not valid_pwd:
        errs.append("JENKINS_PASSWORD is not set")
        
    if not valid_user:
        errs.append("JENKINS_USER is not set")
    
    valid_conn = _conn(errs)    
    valid_params = valid_url and valid_pwd and valid_user
    return HealthResponse(params=valid_params, connection=valid_conn, errors=errs)


def _conn(e: List[str]) -> bool:
    try:
        resp = list_jenkins_plugins()
        return resp is not None and resp.status_code == 200
    except Exception as e:
        log.error("[error]", exception=str(e))
        e.append(f"faild to connect to jenkins: {str(e)}")
        return False


def _param(p: str) -> bool:
    return p is not None and p != ""


