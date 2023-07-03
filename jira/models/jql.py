from pydantic import BaseModel
from typing import List, Any
class RunJQLParams(BaseModel):
    jql_query: str

class RunJQLResponse(BaseModel):
    issues: List[Any]