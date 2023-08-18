from pydantic import BaseModel
from typing import Optional, Literal

class ListOncallsInput(BaseModel):
    pass

class ListOncallsOutput(BaseModel):
    user: dict
    schedule: dict
    escalation_policy: dict
    # ... other optional fields ...

class GetOncallInput(BaseModel):
    oncall_id: str

from pydantic import BaseModel

class CurrentOnCallInput(BaseModel):
    pass

class CurrentOnCallOutput(BaseModel):
    user_id: str
    user_name: str
    user_email: str
    escalation_policy_name: str
    schedule_name: str
