from pydantic import BaseModel
from typing import Optional

class ListSchedulesInput(BaseModel):
    pass

class ListSchedulesOutput(BaseModel):
    id: str
    name: str
    # ... other optional fields ...

class GetScheduleInput(BaseModel):
    schedule_id: str
