from pydantic import BaseModel, constr
from typing import List, Optional


class CreateInstanceRequest(BaseModel):
    image_id: str = "ami-df5de72bdb3b"
    instance_type: constr(regex=r'^(t2\.micro|t2\.small|m4\.large)$')  # Add more allowed instance types
    max_count: int = 1
    min_count: int = 1


class CreateInstanceResponse(BaseModel):
    instance_id: str


class ListInstancesRequest(BaseModel):
    pass
    # instance_ids: Optional[List[str]] = None
    # instance_types: Optional[List[str]] = None


class ListInstancesResponse(BaseModel):
    instances: List[dict]


class RebootInstanceRequest(BaseModel):
    instance_id: str


class RebootInstanceResponse(BaseModel):
    message: str


class DescribeSecurityGroupsRequest(BaseModel):
    instance_id: str


class DescribeSecurityGroupsResponse(BaseModel):
    security_groups: List[dict]