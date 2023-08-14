from pydantic import BaseModel
from typing import Optional

class GetUserInput(BaseModel):
    user_id: str

class CreateUserInput(BaseModel):
    email: str
    name: str
    role: Optional[str] = "user"  # default role
    # ... other optional fields ...

class ListUsersOutput(BaseModel):
    id: str
    name: str
    email: str
