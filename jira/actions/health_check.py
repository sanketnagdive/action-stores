from typing import List
from pydantic import BaseModel
from .. import action_store as s
from ..secrets import get_jira_secrets
from ..jira_wrapper import get_jira_instance


class HealthRequest(BaseModel):
    pass


class HealthResponse(BaseModel):
    params: bool
    connection: bool
    errors: List[str]


@s.kubiya_action()
def health_check(_: HealthRequest) -> HealthResponse:
    errors = List[str]
    params = _validate_params(errors)
    connection = _validate_conn(errors)
    return HealthResponse(params=params, connection=connection, errors=errors)


def _validate_conn(e: List[str]) -> bool:
    try:
        resp = get_jira_instance()
        return resp is not None and resp.status_code == 200
    except Exception as e:
        e.append(f"faild to connect to jira: {str(e)}")
        return False


def _validate_params(e: List[str]) -> bool:
    valid = True
    if s.secrets.get("JIRA_URL") == "":
        valid = False
        e.append("JIRA_URL is not set")

    if s.secrets.get("JIRA_USERNAME") == "":
        valid = False
        e.append("JIRA_USERNAME is not set")

    if s.secrets.get("JIRA_PASSWORD") == "":
        valid = False
        e.append("JIRA_PASSWORD is not set")

    return valid
