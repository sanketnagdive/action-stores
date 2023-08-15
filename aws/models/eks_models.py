from pydantic import BaseModel
from typing import List, Optional


class VpcConfig(BaseModel):
    subnetIds: List[str] = ["subnet-12345678", "subnet-87654321"]  # Placeholder subnet IDs
    securityGroupIds: List[str] = ["sg-12345678"]  # Placeholder security group IDs
    endpointPublicAccess: bool = True
    endpointPrivateAccess: bool = False
    publicAccessCidrs: List[str] = ["0.0.0.0/0"]

class CreateClusterRequest(BaseModel):
    name: str
    roleArn: str
    resourcesVpcConfig: VpcConfig = VpcConfig()

class CreateClusterResponse(BaseModel):
    cluster_name: str


class DeleteClusterRequest(BaseModel):
    cluster_name: str


class DeleteClusterResponse(BaseModel):
    cluster_name: str


class DescribeClusterRequest(BaseModel):
    cluster_name: str


class DescribeClusterResponse(BaseModel):
    cluster: dict


class ListClustersRequest(BaseModel):
    pass


class ListClustersResponse(BaseModel):
    clusters: List[str]
