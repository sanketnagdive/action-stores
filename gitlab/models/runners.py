from typing import List, Any, Optional, Union, Dict, Union
from pydantic import BaseModel, Field
from datetime import datetime

class ListDict(BaseModel):
    response: List[dict]

class SingleDict(BaseModel):
    response: dict

# class ProjectStatInput(BaseModel):
#     id: Union[int,str]

class ListOwnedRunners(BaseModel):
    scope: Optional[str]
    type: Optional[str]
    status: Optional[str] 
    paused: Optional[bool] 
    tag_list: Optional[List[str]]

class ListAllRunners(BaseModel):
    scope: Optional[str]
    type: Optional[str]
    status: Optional[str] 
    paused: Optional[bool] 
    tag_list: Optional[List[str]]

class RunnerId(BaseModel):
    id: int 

# class RunnerUpdate(BaseModel):
#     id: int 
#     description: Optional[str]
#     active: Optional[bool]
#     paused: Optional[bool] 
#     tag_list: Optional[List[str]]
#     run_untagged: Optional[bool] 
#     locked: Optional[bool] 
#     access_level: Optional[str]
#     maximum_timeout: Optional[int]

# class RunnerPause(BaseModel):
#     runner_id: int
#     paused: bool

# class RunnerJobsFilter(BaseModel):
#     id: int 
#     status: Optional[str] 
#     order_by: Optional[str] 
#     sort: Optional[str] 

# class ProjectRunnersFilter(BaseModel):
#     id: Union[int, str] 
#     scope: Optional[str] 
#     type: Optional[str] 
#     status: Optional[str] 
#     paused: Optional[bool] 
#     tag_list: Optional[List[str]] 

# class EnableRunnerInProject(BaseModel):
#     id: Union[int, str] 
#     runner_id: int 
# class DisableRunnerFromProject(BaseModel):
#     id: Union[int, str] 
#     runner_id: int 
# class GroupRunnersFilter(BaseModel):
#     id: int 
#     type: Optional[str] 
#     status: Optional[str] 
#     paused: Optional[bool] 
#     tag_list: Optional[List[str]] 
# class RegisterRunner(BaseModel):
#     token: str 
#     description: Optional[str]
#     info: Optional[dict] 
#     active: Optional[bool] 
#     paused: Optional[bool] 
#     locked: Optional[bool]
#     run_untagged: Optional[bool] 
#     tag_list: Optional[List[str]]
#     access_level: Optional[str] 
#     maximum_timeout: Optional[int]
#     maintainer_note: Optional[str] 
#     maintenance_note: Optional[str] 
# class RunnerToken(BaseModel):
#     token: str 
# class VerifyRunnerAuthentication(BaseModel):
#     token: str 
#     system_id: Optional[str] 
# class ProjectId(BaseModel):
#     id: Union[int, str] 