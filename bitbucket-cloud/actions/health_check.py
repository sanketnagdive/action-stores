from typing import List
from pydantic import BaseModel
from . import action_store as s
from .bitbucket_actions import get_client


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
    space = s.secrets["BITBUCKET_SPACE"]
    try:
        c = get_client(space)
        return c.get_user().login != ""
    except Exception as e:
        e.append(f"faild to connect to bitbucket: {str(e)}")
        return False


def _validate_params(e: List[str]) -> bool:
    valid = True
    if s.secrets.get("BITBUCKET_SPACE") == "":
        valid = False
        e.append("BITBUCKET_SPACE is not set")

    if s.secrets.get("BITBUCKET_USERNAME") == "":
        valid = False
        e.append("BITBUCKET_USERNAME is not set")

    if s.secrets.get("BITBUCKET_APP_PASSWORD") == "":
        valid = False
        e.append("BITBUCKET_APP_PASSWORD is not set")

    return valid
