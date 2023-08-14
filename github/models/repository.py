from pydantic import BaseModel
from typing import List
from . import GitHubPlayGroundRepos,TEST_REPOS

class ListRepositoriesParams(BaseModel):
    pass

class ListRepositoriesResponse(BaseModel):
    repos: List[str]


class CreateRepoParams(BaseModel):
    repo_name: str

class CreateRepoResponse(BaseModel):
    repo_url: str
    # Other fields from repo.raw_data

class DeleteRepoParams(BaseModel):
    repo_name: str

class DeleteRepoResponse(BaseModel):
    success: bool

class GetRepoFilesParams(BaseModel):
    repo_name: GitHubPlayGroundRepos

class GetRepoFilesResponse(BaseModel):
    files: list

class CreatePullRequestParams(BaseModel):
    repo_name: GitHubPlayGroundRepos
    title: str
    body: str
    branch_name: str="main2"

class CreatePullRequestResponse(BaseModel):
    pull_request_url: str


class ListRepositoriesParams(BaseModel):
    pass

class ListRepositoriesResponse(BaseModel):
    repos: List[str]

class FindRepositoriesParams(BaseModel):
    pattern: str=TEST_REPOS

class FindRepositoriesResponse(BaseModel):
    repos: List[str]

class GetRepoBranchesParams(BaseModel):
    repo_name: GitHubPlayGroundRepos

class GetRepoBranchesResponse(BaseModel):
    branches: List[str]