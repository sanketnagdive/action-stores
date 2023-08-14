from pydantic import BaseModel
from typing import List
from . import DEFAULT_BB_WORKSPACE , BitBucketPlayGroundRepos , BitBucketPlayGroundWorkspace
class GetRepositoryBranchesParams(BaseModel):
    workspace: BitBucketPlayGroundWorkspace
    repository_slug: BitBucketPlayGroundRepos

class Branch(BaseModel):
    name: str
    # author: str
    merge_strategies: List[str]
    default_merge_strategy: str

class GetRepositoryBranchesResponse(BaseModel):
    branches: List[Branch]