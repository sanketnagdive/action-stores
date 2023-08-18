from pydantic import BaseModel
from typing import Optional

class ListPoliciesInput(BaseModel):
    pass

class ListPoliciesOutput(BaseModel):
    id: str
    name: str
    escalation_rules: list
    # ... other optional fields ...

class GetPolicyInput(BaseModel):
    policy_id: str
