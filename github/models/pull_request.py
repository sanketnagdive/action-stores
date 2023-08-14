from pydantic import BaseModel
from typing import List
from . import GitHubPlayGroundRepos,TEST_REPOS

class ListOpenPRsParams(BaseModel):
    repo_name: GitHubPlayGroundRepos

class ListOpenPRsResponse(BaseModel):
    prs: List[str]

class GetPRDetailsParams(BaseModel):
    repo_name: GitHubPlayGroundRepos
    pr_number: int

class GetPRDetailsResponse(BaseModel):
    pr_url: str
    title: str
    body: str
    state: str

class GetRepoPullRequestsParams(BaseModel):
    repo_name: GitHubPlayGroundRepos
    state: str  # State can be "open", "closed", or "all"

class PullRequestModel(BaseModel):
    html_url: str
    title: str
    state: str
    created_at: str
    updated_at: str
    merged: bool
    merged_at: str
    merge_commit_sha: str

class GetRepoPullRequestsResponse(BaseModel):
    prs: List[PullRequestModel]

class MergePRParams(BaseModel):
    repo_name: GitHubPlayGroundRepos
    pr_number: int
    commit_message: str
    merge_method: str
    class Config:
        schema_extra = {
            "example": {
                "repo_name": "owner/repo",
                "pr_number": 123,
                "commit_message": "Merge pull request",
                "merge_method": "merge"  # Can be one of: merge, squash, rebase
            }
        }

class MergePRResponse(BaseModel):
    message: str
