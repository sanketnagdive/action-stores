from pydantic import BaseModel
from typing import List

class ListOpenPRsParams(BaseModel):
    repo_name: str

class ListOpenPRsResponse(BaseModel):
    prs: List[str]

class GetPRDetailsParams(BaseModel):
    repo_name: str
    pr_number: int

class GetPRDetailsResponse(BaseModel):
    pr_url: str
    title: str
    body: str
    state: str

class GetRepoPullRequestsParams(BaseModel):
    repo_name: str
    state: str  # State can be "open", "closed", or "all"

class PullRequestModel(BaseModel):
    html_url: str
    title: str
    state: str

class GetRepoPullRequestsResponse(BaseModel):
    prs: List[PullRequestModel]