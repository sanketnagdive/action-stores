from typing import List, Any, Optional, Union, Dict, Union
from pydantic import BaseModel, Field
from datetime import datetime

class ListDict(BaseModel):
    response: List[dict]

class SingleDict(BaseModel):
    response: dict

class GetFileFromRepository(BaseModel):
    id: Union[int, str]
    file_path: str
    ref: str
    
class GetFileBlameFromRepository(BaseModel):
    id: Union[int, str] 
    file_path: str 
    ref: str 
    range_start: int 
    range_end: int 
    range: Optional[dict]

class GetRawFileFromRepository(BaseModel):
    id: Union[int, str]
    file_path: str 
    ref: str 
    lfs: Optional[bool] 

class CreateNewFileInRepository(BaseModel):
    branch: str
    commit_message: str
    content: str
    file_path: str 
    id: Union[int, str]
    author_email: Optional[str] 
    author_name: Optional[str]
    encoding: Optional[str] 
    execute_filemode: Optional[bool] 
    start_branch: str  
