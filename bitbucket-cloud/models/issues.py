from pydantic import BaseModel
from typing import List
from . import DEFAULT_BB_WORKSPACE

class GetIssueParams(BaseModel):
    workspace: str=DEFAULT_BB_WORKSPACE
    repository_slug: str
    issue_id: str

class GetIssueResponse(BaseModel):
    issue: dict


class GetIssuesParams(BaseModel):
    workspace: str=DEFAULT_BB_WORKSPACE
    repository_slug: str

class GetIssuesResponse(BaseModel):
    issues: List[dict]

class CreateIssueParams(BaseModel):
    workspace: str=DEFAULT_BB_WORKSPACE
    repo_slug: str
    type: str
    title: str
    content: str
    priority: str

class CreateIssueResponse(BaseModel):
    issue: dict

class DeleteIssueParams(BaseModel):
    workspace: str=DEFAULT_BB_WORKSPACE
    repo_slug: str
    issue_id: str

class DeleteIssueResponse(BaseModel):
    issue: dict