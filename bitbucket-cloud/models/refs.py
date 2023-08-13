from pydantic import BaseModel
from typing import List
from . import DEFAULT_BB_WORKSPACE
class GetRepositoryBranchesParams(BaseModel):
    workspace: str= DEFAULT_BB_WORKSPACE
    repository_slug: str

class Branch(BaseModel):
    name: str
    # author: str
    merge_strategies: List[str]
    default_merge_strategy: str

class GetRepositoryBranchesResponse(BaseModel):
    branches: List[Branch]