from pydantic import BaseModel
from typing import List


class TerminateInstanceRequest(BaseModel):
    instance_id: str


class TerminateInstanceResponse(BaseModel):
    message: str


class CreateInstanceRequest(BaseModel):
    image_id: str
    instance_type: str
    min_count: int
    max_count: int


class CreateInstanceResponse(BaseModel):
    instance_id: str


class ListInstancesRequest(BaseModel):
    instance_ids: List[str] = None
    instance_types: List[str] = None


class ListInstancesResponse(BaseModel):
    instances: List[dict]
