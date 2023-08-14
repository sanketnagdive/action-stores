from pydantic import BaseModel,Field
from typing import List
from . import DEFAULT_BB_WORKSPACE , BitBucketPlayGroundRepos, DEFAULT_BRANCH, BitBucketPlayGroundWorkspace

class GetPipelineRequest(BaseModel):
    workspace: BitBucketPlayGroundWorkspace
    repo_slug: BitBucketPlayGroundRepos
    pipeline_uuid: str


class GetPipelineResponse(BaseModel):
    pipeline: dict

class GetPipelinesRequest(BaseModel):
    workspace: BitBucketPlayGroundWorkspace
    repo_slug: BitBucketPlayGroundRepos


class GetPipelinesResponse(BaseModel):
    pipelines: List[dict]


class RunPipelineRequest(BaseModel):
    workspace: BitBucketPlayGroundWorkspace
    repo_slug: BitBucketPlayGroundRepos
    branch_name: str=DEFAULT_BRANCH

class RunPipelineResponse(BaseModel):
    run: dict

class StopPipelineRequest(BaseModel):
    workspace: BitBucketPlayGroundWorkspace
    repo_slug: BitBucketPlayGroundRepos
    pipeline_uuid: str

class StopPipelineResponse(BaseModel):
    run: dict