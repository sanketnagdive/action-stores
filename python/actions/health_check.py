import logging as log
from typing import List

from pydantic import BaseModel
from . import actionstore as action_store
from .interpreter import execute_python_code

class HealthRequest(BaseModel):
    pass

class HealthResponse(BaseModel):
    params: bool
    connection: bool
    errors: List[str]

@action_store.kubiya_action()
def health_check(_) -> HealthResponse:
    output = True
    excepted='run python code'
    code = 'print("run python code")'
    
    result = execute_python_code(code, output)
    if 'error' in result:
        log.error("Error: - %s", result['error'])
        log.error("Traceback: - %s", result['traceback'])
        return HealthResponse(params=True, connection=False, errors=[result['error']])
    else:
        return HealthResponse(params=True, connection=excepted in result['output'])
