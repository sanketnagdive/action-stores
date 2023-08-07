from pydantic import BaseModel
from typing import List

class GetOpenPullRequestsParams(BaseModel):
    workspace: str
    repository_slug: str

class GetOpenPullRequestsResponse(BaseModel):
    pull_requests: List[dict]


class MergePrParams(BaseModel):
    workspace: str
    repository_slug: str
    pull_request_id: str

class MergePrResponse(BaseModel):
    response: dict


class CreatePrParams(BaseModel):
    workspace: str
    repository_slug: str
    title: str
    source_branch: str
    destination_branch: str

class CreatePrResponse(BaseModel):
    response: dict