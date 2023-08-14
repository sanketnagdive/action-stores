from pydantic import BaseModel
from typing import List
from . import DEFAULT_BB_WORKSPACE,BitBucketPlayGroundRepos,DEFAULT_BRANCH

class GetFileContentParams(BaseModel):
    workspace: str = DEFAULT_BB_WORKSPACE
    repository: BitBucketPlayGroundRepos
    file_path: str
    commit_id: str

class GetFileContentResponse(BaseModel):
    content: str


class UploadFileParams(BaseModel):
    workspace: str=DEFAULT_BB_WORKSPACE
    repository_slug: str
    branch: str
    commit_message: str
    file_path: str
    file_content: str

class UploadFileResponse(BaseModel):
    pass



class RepositoryStructure(BaseModel):
    path: str
    commit_hash: str

class GetRepositoryStructureParams(BaseModel):
    workspace: str= DEFAULT_BB_WORKSPACE
    repository_slug: BitBucketPlayGroundRepos
    branch_or_commit: str=DEFAULT_BRANCH
    path: str=""

class GetRepositoryStructureResponse(BaseModel):
    structure: List[RepositoryStructure]