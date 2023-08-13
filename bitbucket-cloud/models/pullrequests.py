from pydantic import BaseModel
from typing import List
from . import DEFAULT_BB_WORKSPACE
class GetOpenPullRequestsParams(BaseModel):
    workspace: str= DEFAULT_BB_WORKSPACE
    repository_slug: str

class GetOpenPullRequestsResponse(BaseModel):
    pull_requests: List[dict]


class MergePrParams(BaseModel):
    workspace: str= DEFAULT_BB_WORKSPACE
    repository_slug: str
    pull_request_id: str

class MergePrResponse(BaseModel):
    response: dict


class CreatePrParams(BaseModel):
    workspace: str= DEFAULT_BB_WORKSPACE
    repository_slug: str
    title: str
    source_branch: str
    destination_branch: str

class CreatePrResponse(BaseModel):
    response: dict