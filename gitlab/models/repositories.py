from typing import List, Any, Optional, Union, Dict
from pydantic import BaseModel, Field
from datetime import datetime

class ListDict(BaseModel):
    response: List[dict]

class SingleDict(BaseModel):
    response: dict

class ListRepositoryTree(BaseModel):
    id: Union[int, str]
    page_token: Optional[str]
    pagination: Optional[str]
    path: Optional[str]
    per_page: Optional[int] = 20
    recursive: Optional[bool] = False
    ref: Optional[str]

class GetABlobFromRepository(BaseModel):
    id: Union[int, str]
    sha: str

class CompareBranchesTagsOrCommits(BaseModel):
    id: Union[int, str] = Field(description='The ID or URL-encoded path of the project owned by the authenticated user.')
    from_commit_or_branch: str = Field(..., alias='from', description='The commit SHA or branch name.')
    to: str = Field(..., description='The commit SHA or branch name.')
    from_project_id: Optional[int] = Field(None, description='The ID to compare from.')
    straight: Optional[bool] = Field(False, description='Comparison method: true for direct comparison between from and to (from..to), false to compare using merge base (from…to)’. Default is false.')


class GetContributors(BaseModel):
    id: Union[int, str] = Field(description='The ID or URL-encoded path of the project owned by the authenticated user.')
    order_by: Optional[str] = Field(None, description='Return contributors ordered by name, email, or commits (orders by commit date) fields. Default is commits.')
    sort: Optional[str] = Field(None, description='Return contributors sorted in asc or desc order. Default is asc.')

class GetMergeBase(BaseModel):
    id: Union[int, str] = Field(description='The ID or URL-encoded path of the project.')
    refs: List[str] = Field(description='The refs to find the common ancestor of. Accepts multiple refs.')