from pydantic import BaseModel
from typing import List
class GetRepositoryBranchesParams(BaseModel):
    workspace: str
    repository_slug: str

class Branch(BaseModel):
    name: str
    # author: str
    merge_strategies: List[str]
    default_merge_strategy: str

class GetRepositoryBranchesResponse(BaseModel):
    branches: List[Branch]