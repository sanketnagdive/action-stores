from typing import List, Any, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from ..models.repository_files import *

from .. import action_store as action_store
from ..http_wrapper import *

@action_store.kubiya_action()
def get_file_from_repository(input: GetFileFromRepository):
    response = get_wrapper(endpoint=f'/projects/{input.id}/repository/files/{input.file_path}', args=input.dict(exclude_none=True))
    return SingleDict(response=response)

@action_store.kubiya_action()
def get_file_blame_from_repository(input: GetFileBlameFromRepository):
    response = get_wrapper(endpoint=f'/projects/{input.id}/repository/files/{input.file_path}/blame', args=input.dict(exclude_none=True))
    return ListDict(response=response)

@action_store.kubiya_action()
def get_raw_file_from_repository(input: GetRawFileFromRepository):
    response = get_wrapper(endpoint=f'/projects/{input.id}/repository/files/{input.file_path}/raw', args=input.dict(exclude_none=True))
    return SingleDict(response=response)

@action_store.kubiya_action()
def create_new_file_in_repository(input: CreateNewFileInRepository):
    response = post_wrapper(endpoint=f'/projects/{input.id}/repository/files/{input.file_path}', args=input.dict(exclude_none=True))
    return SingleDict(response=response)
