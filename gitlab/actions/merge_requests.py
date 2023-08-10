from typing import List, Any, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from ..models.merge_requests import *

from .. import action_store as action_store
from ..http_wrapper import *

@action_store.kubiya_action()
def list_merge_requests(input: ListMergeRequests):
    response = get_wrapper(endpoint='/merge_requests', args=input.dict(exclude_none=True, by_alias=True))
    return ListDict(response=response)

@action_store.kubiya_action()
def list_project_merge_requests(input: ListProjectMergeRequests):
    response = get_wrapper(endpoint=f'/projects/{input.id}/merge_requests', args=input.dict(exclude_none=True, by_alias=True))
    return ListDict(response=response)

@action_store.kubiya_action()
def list_group_merge_requests(input: ListGroupMergeRequests):
    response = get_wrapper(endpoint=f'/groups/{input.id}/merge_requests', args=input.dict(exclude_none=True, by_alias=True))
    return ListDict(response=response)

@action_store.kubiya_action()
def get_single_mr(input: GetSingleMR):
    response = get_wrapper(endpoint=f'/projects/{input.id}/merge_requests/{input.merge_request_iid}', args=input.dict(exclude_none=True))
    return SingleDict(response=response)

@action_store.kubiya_action()
def get_merge_request_commits(input: GetMergeRequestCommits):
    response = get_wrapper(endpoint=f'/projects/{input.id}/merge_requests/{input.merge_request_iid}/commits')
    return ListDict(response=response)

@action_store.kubiya_action()
def get_merge_request_changes(input: GetMergeRequestChanges):
    response = get_wrapper(endpoint=f'/projects/{input.id}/merge_requests/{input.merge_request_iid}/changes', args=input.dict(exclude_none=True))
    return ListDict(response=response)

@action_store.kubiya_action()
def list_merge_request_diffs(input: ListMergeRequestDiffs):
    response = get_wrapper(endpoint=f'/projects/{input.id}/merge_requests/{input.merge_request_iid}/diffs', args=input.dict(exclude_none=True))
    return ListDict(response=response)

@action_store.kubiya_action()
def list_merge_request_pipelines(input: ListMergeRequestPipelines):
    response = get_wrapper(endpoint=f'/projects/{input.id}/merge_requests/{input.merge_request_iid}/pipelines')
    return ListDict(response=response)

@action_store.kubiya_action()
def create_merge_request_pipeline(input: CreateMergeRequestPipeline):
    response = post_wrapper(endpoint=f'/projects/{input.id}/merge_requests/{input.merge_request_iid}/pipelines', args=input.dict())
    return SingleDict(response=response)

@action_store.kubiya_action()
def create_new_merge_request(input: ProjectsMergeRequestCreate):
    response = post_wrapper(endpoint=f'/projects/{input.id}/merge_requests', args=input.dict(exclude_none=True))
    return SingleDict(response=response)

@action_store.kubiya_action()
def update_merge_request(input: UpdateMergeRequest):
    response = put_wrapper(endpoint=f'/projects/{input.id}/merge_requests/{input.merge_request_iid}', args=input.dict(exclude_none=True))
    return SingleDict(response=response)

@action_store.kubiya_action()
def delete_merge_request(input: DeleteMergeRequest):
    response = delete_wrapper(endpoint=f'/projects/{input.id}/merge_requests/{input.merge_request_iid}', args=input.dict(exclude_none=True))
    return SingleDict(response=response)

@action_store.kubiya_action()
def merge_merge_request(input: MergeMergeRequest):
    response = put_wrapper(endpoint=f'/projects/{input.id}/merge_requests/{input.merge_request_iid}/merge', args=input.dict(exclude_none=True))
    return SingleDict(response=response)

@action_store.kubiya_action()
def rebase_merge_request(input: RebaseMergeRequest):
    response = put_wrapper(endpoint=f'/projects/{input.id}/merge_requests/{input.merge_request_iid}/rebase', args=input.dict(exclude_none=True))
    return SingleDict(response=response)

@action_store.kubiya_action()
def get_merge_request_diff_versions(input: GetMergeRequestDiffVersions):
    response = get_wrapper(endpoint=f'/projects/{input.id}/merge_requests/{input.merge_request_iid}/versions', args=input.dict(exclude_none=True))
    return ListDict(response=response)

@action_store.kubiya_action()
def get_single_merge_request_diff_version(input: GetSingleMergeRequestDiffVersion):
    response = get_wrapper(endpoint=f'/projects/{input.id}/merge_requests/{input.merge_request_iid}/versions/{input.version_id}', args=input.dict(exclude_none=True))
    return SingleDict(response=response)