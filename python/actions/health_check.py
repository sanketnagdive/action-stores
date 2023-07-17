import logging as log
from . import actionstore as action_store
from .interpreter import execute_python_code


@action_store.kubiya_action()
def health_check() -> bool:
    output = True
    excepted='run python code'
    code = 'print("run python code")'
    
    result = execute_python_code(code, output)
    if 'error' in result:
        log.error("Error: - %s", result['error'])
        log.error("Traceback: - %s", result['traceback'])
        return False
    else:
        return excepted in result['output']
