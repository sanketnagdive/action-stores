from pydantic import BaseModel, constr
from .common import SimpleResponse
from typing import List, Optional


class CreateIssueParams(BaseModel):
    issue_type_name: constr(regex=r'^(Bug|Task|Story|Epic)$')
    summary: str
    description: str


class CommentIssueParams(BaseModel):
    issue_key: str
    body: str

class TransitionIssueParams(BaseModel):
    issue_key: str
    transition_name: str

class TransitionIssueResponse(SimpleResponse):
    pass

class CreateIssueResponse(BaseModel):
    key: str
    self: str

class GetAllIssuesParams(BaseModel):
    project_key: str

class IssueData(BaseModel):
    key: str
    fields: dict

class GetAllIssuesResponse(BaseModel):
    issues: List[IssueData]

class CommentIssueResponse(BaseModel):
    id: str
    body: str
    author: dict
    created: str

class UpdateIssueParams(BaseModel):
    issue_key: str
    summary: Optional[str] = None
    description: Optional[str] = None

class UpdateIssueResponse(BaseModel):
    success: bool
    message: str

class AssignIssueParams(BaseModel):
    issue_key: str
    assignee_name: constr(regex=r'^(Michael Gonzalez)$') = 'Michael Gonzalez'