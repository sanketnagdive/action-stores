from pydantic import BaseModel
from typing import List
from . import DEFAULT_BB_WORKSPACE, BitBucketPlayGroundWorkspace, BitBucketPlayGroundRepos, DEFAULT_BRANCH


class EditYamlFileParams(BaseModel):
    workspace: BitBucketPlayGroundWorkspace
    template_repository: str
    template_file_path: str
    template_commit_id: str
    kubiya_param_1: str
    kubiya_param_2: str
    destination_repository_slug: str
    destination_branch: str
    commit_message: str
    destination_file_path: str


class EditYamlFileResponse(BaseModel):
    pass