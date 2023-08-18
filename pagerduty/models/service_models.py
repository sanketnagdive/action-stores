from pydantic import BaseModel
from typing import Optional

class ListServicesInput(BaseModel):
    pass

class ListServicesOutput(BaseModel):
    id: str
    name: str
    description: Optional[str]
    # ... other optional fields ...

class GetServiceInput(BaseModel):
    service_id: str
