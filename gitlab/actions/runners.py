from typing import List, Any, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from ..models.runners import *

from .. import action_store as action_store
from ..http_wrapper import *

@action_store.kubiya_action()
def list_owned_runners(input: ListOwnedRunners):
    response = get_wrapper(endpoint='/runners', args=input.dict(exclude_none=True))
    return ListDict(response=response)

@action_store.kubiya_action()
def list_all_runners(input: ListAllRunners):
    response = get_wrapper(endpoint='/runners/all', args=input.dict(exclude_none=True))
    return ListDict(response=response)

@action_store.kubiya_action()
def get_runner_details(input: RunnerId):
    response = get_wrapper(endpoint=f'/runners/{input.id}')
    return SingleDict(response=response)

# @action_store.kubiya_action()
# def update_runner_details(input: RunnerUpdate):
#     response = put_wrapper(endpoint=f'/runners/{input.id}', args=input.dict(exclude_none=True))
#     return SingleDict(response=response)

# @action_store.kubiya_action()
# def pause_runner(input: RunnerPause):
#     response = put_wrapper(endpoint=f'/runners/{input.runner_id}', args=input.dict(exclude_none=True))
#     return ListDict(response=response)

# @action_store.kubiya_action()
# def list_runner_jobs(input: RunnerJobsFilter):
#     response = get_wrapper(endpoint=f'/runners/{input.id}/jobs', args=input.dict(exclude_none=True))
#     return ListDict(response=response)

# @action_store.kubiya_action()
# def list_project_runners(input: ProjectRunnersFilter):
#     response = get_wrapper(endpoint=f'/projects/{input.id}/runners', args=input.dict(exclude_none=True))
#     return ListDict(response=response)

# @action_store.kubiya_action()
# def list_group_runners(input: GroupRunnersFilter):
#     response = get_wrapper(endpoint=f'/groups/{input.id}/runners', args=input.dict(exclude_none=True))
#     return ListDict(response=response)

# @action_store.kubiya_action()
# def verify_runner_authentication(input: VerifyRunnerAuthentication):
#     return post_wrapper(endpoint='/runners/verify', args=input.dict(exclude_none=True))