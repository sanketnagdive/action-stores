import logging as log
from typing import List

from pydantic import BaseModel
from .. import action_store
from ..secrets import get_jira_secrets
from ..jira_wrapper import get_jira_instance

class HealthRequest(BaseModel):
    pass

class HealthResponse(BaseModel):
    params: bool
    connection: bool
    errors: List[str]

@action_store.kubiya_action()
def health_check(_) -> HealthResponse:
    errs = []
    url, user, pwd = get_jira_secrets()
    valid_url = _param(url)
    valid_pwd = _param(pwd)
    valid_user = _param(user)
    
    if not valid_url:
        errs.append("JIRA_URL is not set")
        
    if not valid_pwd:
        errs.append("JIRA_PASSWORD is not set")
        
    if not valid_user:
        errs.append("JIRA_USERNAME is not set")
        
    valid_conn = _conn(errs)
    valid_params = valid_url and valid_pwd and valid_user
    return HealthResponse(params=valid_params, connection=valid_conn, errors=errs)


def _conn(e: List[str]) -> bool:
    try:
        c = get_jira_instance()
        return c.myself()["accountId"] != ""
    except Exception as e:
        log.error("[error]", exception=str(e))
        return False


def _param(p: str) -> bool:
    return p is not None and p != ""

