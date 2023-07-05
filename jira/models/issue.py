from pydantic import BaseModel
from .common import SimpleResponse
from typing import List


class CreateIssueParams(BaseModel):
    project_key: str
    issue_type_name: str
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

class LinkIssuesParams(BaseModel):
    issue_key_1: str
    issue_key_2: str
    link_type_name: str

class LinkIssuesResponse(SimpleResponse):
    pass


class UpdateIssueParams(BaseModel):
    issue_key: str
    update_dict: dict

class UpdateIssueResponse(BaseModel):
    success: bool

class AssignIssueParams(BaseModel):
    issue_key: str
    assignee_name: str

class DeleteIssueParams(BaseModel):
    issue_key: str

class DeleteIssueResponse(BaseModel):
    success: bool