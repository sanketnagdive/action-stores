from pydantic import BaseModel, constr, PositiveInt
from typing import List, Optional


class ListRDSInstancesRequest(BaseModel):
    pass

class ListRDSInstancesResponse(BaseModel):
    instance_names: List[str]


class DescribeRDSSnapshotsRequest(BaseModel):
    snapshot_ids: List[str]


class DescribeRDSSnapshotsResponse(BaseModel):
    snapshots: List[dict]


class CreateRDSInstanceRequest(BaseModel):
    instance_identifier: str
    db_instance_class: constr(regex=r'^db\.(t2|t3|m4|m5|r4|r5)\.(micro|medium|small|large)$')
    engine: constr(regex=r'^(mysql|postgres|oracle)\b$')
    allocated_storage: PositiveInt
    master_username: str
    master_password: str

class CreateRDSInstanceResponse(BaseModel):
    DBInstance: dict
    ResponseMetadata: dict