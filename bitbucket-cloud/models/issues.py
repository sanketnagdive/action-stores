from pydantic import BaseModel
from typing import List


class GetIssueParams(BaseModel):
    workspace: str
    repository_slug: str
    issue_id: str

class GetIssueResponse(BaseModel):
    issue: dict


class GetIssuesParams(BaseModel):
    workspace: str
    repository_slug: str

class GetIssuesResponse(BaseModel):
    issues: List[dict]

class CreateIssueParams(BaseModel):
    workspace: str
    repo_slug: str
    type: str
    title: str
    content: str
    priority: str

class CreateIssueResponse(BaseModel):
    issue: dict

class DeleteIssueParams(BaseModel):
    workspace: str
    repo_slug: str
    issue_id: str

class DeleteIssueResponse(BaseModel):
    issue: dict