import logging as log
from typing import List
from .. import action_store
from pydantic import BaseModel
from ..github_wrapper import get_github_instance, get_entity
from ..secrets import get_github_token, get_github_organization

class HealthRequest(BaseModel):
    pass

class HealthResponse(BaseModel):
    params: bool
    connection: bool
    errors: List[str]

@action_store.kubiya_action()
def health_check(params: HealthRequest) -> HealthResponse:
    errors = []
    valid_params = True
    token = get_github_token()
    org = get_github_organization()
    
    if _param(token) or _param(org):
        if _param(org):
            errors.append("GITHUB_ORGANIZATION is not set")
        if _param(token):
            errors.append("GITHUB_TOKEN is not set")
        valid_params = False
        
    valid_connection = _conn(pwd=token, org=org, errs=errors)
    return HealthResponse(params=valid_params, connection=valid_connection, errors=errors)


def _param(p: str) -> bool:
    return p is not None and p != ""


def _conn(pwd: str, org: str, errs: List[str]) -> bool:        
    try:
        c = get_entity(get_github_instance())
        return c.get_user().login != "" and c.get_organization(org).login != ""
    except Exception as e:
        log.error("[error]", exception=str(e))
        errs.append(f"faild to connect to github: {str(e)}")
        return False

