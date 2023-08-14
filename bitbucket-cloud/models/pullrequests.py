from pydantic import BaseModel
from typing import List
from . import DEFAULT_BB_WORKSPACE, BitBucketPlayGroundRepos , DEFAULT_BRANCH
class GetOpenPullRequestsParams(BaseModel):
    workspace: str= DEFAULT_BB_WORKSPACE
    repository_slug: BitBucketPlayGroundRepos

class GetOpenPullRequestsResponse(BaseModel):
    pull_requests: List[dict]


class MergePrParams(BaseModel):
    workspace: str= DEFAULT_BB_WORKSPACE
    repository_slug: BitBucketPlayGroundRepos
    pull_request_id: str

class MergePrResponse(BaseModel):
    response: dict


class CreatePrParams(BaseModel):
    workspace: str= DEFAULT_BB_WORKSPACE
    repository_slug: BitBucketPlayGroundRepos
    title: str
    source_branch: str
    destination_branch: str=DEFAULT_BRANCH

class CreatePrResponse(BaseModel):
    response: dict