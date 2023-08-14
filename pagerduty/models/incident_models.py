from pydantic import BaseModel
from typing import Optional, List, Any
from typing_extensions import Literal

class IncidentDetails(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    status: str
    service: dict
    assigned_to: List[dict]

class ListIncidentsInput(BaseModel):
    status: Optional[str] = None

class ListIncidentsOutput(IncidentDetails):
    pass

class GetIncidentInput(BaseModel):
    incident_id: str

class ModifyIncidentInput(IncidentDetails):
    pass

class CreateIncidentInput(BaseModel):
    type: str = "incident"
    title: str
    service_id: str
    # priority_id: str = "P1"
    urgency: str = "high"
    body_details: Optional[str]
    incident_key: Optional[str]
