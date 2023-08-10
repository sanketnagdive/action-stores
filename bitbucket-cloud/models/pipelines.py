from pydantic import BaseModel,Field
from typing import List


class GetPipelineRequest(BaseModel):
    workspace: str
    repo_slug: str
    pipeline_uuid: str


class GetPipelineResponse(BaseModel):
    pipeline: dict

class GetPipelinesRequest(BaseModel):
    workspace: str
    repo_slug: str


class GetPipelinesResponse(BaseModel):
    pipelines: List[dict]


class RunPipelineRequest(BaseModel):
    workspace: str
    repo_slug: str
    branch_name: str

class RunPipelineResponse(BaseModel):
    run: dict

class StopPipelineRequest(BaseModel):
    workspace: str
    repo_slug: str
    pipeline_uuid: str

class StopPipelineResponse(BaseModel):
    run: dict