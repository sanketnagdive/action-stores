from .interpreter import execute_python_code
import logging as log

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
