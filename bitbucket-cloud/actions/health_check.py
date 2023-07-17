
import logging as log
from typing import List

from pydantic import BaseModel
from . import action_store
from .bitbucket_actions import get_client

class HealthRequest(BaseModel):
    pass

class HealthResponse(BaseModel):
    params: bool
    connection: bool
    errors: List[str]

@action_store.kubiya_action()
def health_check(_) -> HealthResponse:    
    errs = []
    org = action_store.secrets["BITBUCKET_SPACE"]
    user = action_store.secrets["BITBUCKET_USERNAME"]
    pwd = action_store.secrets["BITBUCKET_APP_PASSWORD"]
    
    valid_pwd = _param(pwd)
    valid_org = _param(org)
    valid_user = _param(user)
    
    if not valid_pwd:
        errs.append("BITBUCKET_APP_PASSWORD is not set")
        
    if not valid_org:
        errs.append("BITBUCKET_SPACE is not set")
        
    if not valid_user:
        errs.append("BITBUCKET_USERNAME is not set")
    
    valid_conn = _conn(org, errs)
    valid_params = valid_pwd and valid_org and valid_user
    return HealthResponse(params=valid_params, connection=valid_conn, errors=errs)

def _conn(v: str, e: List[str]) -> bool:
    try:
        c = get_client(v)
        return c.get_user().login != ""
    except Exception as e:
        log.error("[error]", exception=str(e))
        e.append(f"faild to connect to bitbucket: {str(e)}")
        return False


def _param(p: str) -> bool:
    return p is not None and p != ""

