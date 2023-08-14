from pydantic import BaseModel
from typing import List
from . import DEFAULT_BB_WORKSPACE , BitBucketPlayGroundRepos, BitBucketPlayGroundWorkspace

class GetIssueParams(BaseModel):
    workspace: BitBucketPlayGroundWorkspace
    repository_slug: BitBucketPlayGroundRepos
    issue_id: str

class GetIssueResponse(BaseModel):
    issue: dict


class GetIssuesParams(BaseModel):
    workspace: BitBucketPlayGroundWorkspace
    repository_slug: BitBucketPlayGroundRepos

class GetIssuesResponse(BaseModel):
    issues: List[dict]

class CreateIssueParams(BaseModel):
    workspace: BitBucketPlayGroundWorkspace
    repo_slug: BitBucketPlayGroundRepos
    type: str
    title: str
    content: str
    priority: str

class CreateIssueResponse(BaseModel):
    issue: dict

class DeleteIssueParams(BaseModel):
    workspace: BitBucketPlayGroundWorkspace
    repo_slug: BitBucketPlayGroundRepos
    issue_id: str

class DeleteIssueResponse(BaseModel):
    issue: dict