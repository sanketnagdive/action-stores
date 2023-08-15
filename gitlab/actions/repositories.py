from typing import List, Any, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from ..models.repositories import *

from .. import action_store as action_store
from ..http_wrapper import *

@action_store.kubiya_action()
def list_repository_tree(input: ListRepositoryTree):
    response = get_wrapper(endpoint=f'/projects/{input.id}/repository/tree', args=input.dict(exclude_none=True))
    return ListDict(response=response)

@action_store.kubiya_action()
def get_a_blob_from_repository(input: GetABlobFromRepository):
    return get_wrapper(endpoint=f'/projects/{input.id}/repository/blobs/{input.sha}', args=input.dict(exclude_none=True))

@action_store.kubiya_action()
def raw_blob_content(input: GetABlobFromRepository):
    return get_wrapper(endpoint=f'/projects/{input.id}/repository/blobs/{input.sha}/raw', args=input.dict(exclude_none=True))

@action_store.kubiya_action()
def compare_branches_tags_or_commits(input: CompareBranchesTagsOrCommits):
    response =  get_wrapper(endpoint=f'/projects/{input.id}/repository/compare', args=input.dict(exclude_none=True, by_alias=True))
    return SingleDict(response=response)

@action_store.kubiya_action()
def get_contributors(input: GetContributors):
    response = get_wrapper(endpoint=f'/projects/{input.id}/repository/contributors', args=input.dict(exclude_none=True))
    return ListDict(response=response)

@action_store.kubiya_action()
def get_merge_base(input: GetMergeBase):
    response = get_wrapper(endpoint=f'/projects/{input.id}/repository/merge_base', args={'refs[]': input.refs})
    return SingleDict(response=response)