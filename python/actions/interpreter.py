import sys
import traceback
from typing import Optional
from pydantic import BaseModel
from . import actionstore as action_store
import logging as log

class ExecuteCodeInput(BaseModel):
    code: str
    capture_output: bool = False

def execute_python_code(code, capture_output=False):
    try:
        # Create a restricted globals dictionary
        restricted_globals = {
            '__builtins__': {},
        }

        # Create a restricted locals dictionary
        restricted_locals = {}

        # Capture output if requested
        if capture_output:
            stdout_buffer = []
            restricted_globals['print'] = lambda *args, **kwargs: stdout_buffer.append(' '.join(map(str, args)))
        else:
            restricted_globals['print'] = lambda *args, **kwargs: None

        # Execute the code in the restricted environment
        exec(code, restricted_globals, restricted_locals)

        # Return the result of the execution
        if capture_output:
            return {
                'result': restricted_locals,
                'output': '\n'.join(stdout_buffer)
            }
        else:
            return {'result': restricted_locals}

    except Exception as e:
        # Handle any exceptions that occur during execution
        error_traceback = traceback.format_exc()
        return {'error': str(e), 'traceback': error_traceback}


@action_store.kubiya_action(validate_input=False)
def execute_code(action_input: ExecuteCodeInput):
    code = action_input.code
    capture_output = action_input.capture_output
    res = execute_python_code(code, capture_output=capture_output)
    if 'error' in res:
        log.error("An error occurred: - %s", res['error'])
        log.error("Traceback: - %s", res['traceback'])
        return {'error': res['error'], 'traceback': res['traceback']}
    else:
        log.info("Execution successful")
        if 'output' in res:
            log.info("Output: - %s", res['output'])
            return res['output']
        else:
            log.info("Result: - %s", res['result'])
        return {'result': res['result']}