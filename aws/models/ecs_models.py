from pydantic import BaseModel
from typing import List, Optional


class RegisterTaskDefinitionRequest(BaseModel):
    family: str
    taskRoleArn: str
    executionRoleArn: str
    networkMode: str
    containerDefinitions: List[dict]
    placementConstraints: List[dict] = None
    requiresCompatibilities: List[str] = None
    cpu: str = None
    memory: str = None
    volumes: List[dict] = None
    placementStrategy: List[dict] = None
    tags: List[dict] = None


class RegisterTaskDefinitionResponse(BaseModel):
    task_definition: dict


class DescribeTaskDefinitionRequest(BaseModel):
    task_definition_arn: str


class DescribeTaskDefinitionResponse(BaseModel):
    task_definition: dict


class ListTaskDefinitionsRequest(BaseModel):
    family_prefix: Optional[str] = None
    status: Optional[str] = None
    sort: Optional[str] = None
    max_results: Optional[int] = None
    next_token: Optional[str] = None


class ListTaskDefinitionsResponse(BaseModel):
    task_definitions: List[str]


class DescribeECSClustersRequest(BaseModel):
    cluster_names: List[str] = None


class DescribeECSClustersResponse(BaseModel):
    clusters: List[dict]


class ListECSServicesRequest(BaseModel):
    cluster_name: str
    service_names: List[str] = None


class ListECSServicesResponse(BaseModel):
    services: List[dict]


class CreateECSClusterRequest(BaseModel):
    cluster_name: str


class CreateECSClusterResponse(BaseModel):
    cluster_arn: str


class ListECSClustersRequest(BaseModel):
    pass

class ListECSClustersResponse(BaseModel):
    cluster_arns: list