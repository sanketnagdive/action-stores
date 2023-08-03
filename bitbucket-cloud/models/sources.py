from pydantic import BaseModel
from typing import List


class GetFileContentParams(BaseModel):
    workspace: str
    repository: str
    file_path: str
    commit_id: str

class GetFileContentResponse(BaseModel):
    content: str