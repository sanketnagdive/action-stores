from pydantic import BaseModel, Field
from typing import Optional, List

class ListAccounts(BaseModel):
    pass

class GetAccounts(BaseModel):
    name: str = Field(default = "")

class ListApplicationsInput(BaseModel):
    name: Optional[str] = None
    refresh: Optional[str] = None
    projects: Optional[List[str]] = None
    resourceVersion: Optional[str] = None
    selector: Optional[str] = None
    repo: Optional[str] = None
    appNamespace: Optional[str] = None
    project: Optional[List[str]] = None

class SyncName(BaseModel):
    name: str

class ListProjects(BaseModel):
    pass

class ListProjectsName(BaseModel):
    name: str
