from typing import List

from pydantic import BaseModel

from . import actionstore as s
from .interpreter import execute_python_code


class HealthRequest(BaseModel):
    pass


class HealthResponse(BaseModel):
    params: bool
    connection: bool
    errors: List[str]


@s.kubiya_action()
def health_check(_: HealthRequest) -> HealthResponse:
    valid = True
    errors = List[str]
    excepted = "run python code"
    code = 'print("run python code")'

    result = execute_python_code(code, True)
    if "error" not in result:
        valid = excepted in str(result["output"])
    else:
        valid = False
        err = str(result["error"])
        errors.append(f"faild to run python: {err}")

    return HealthResponse(params=True, connection=valid, errors=errors)
