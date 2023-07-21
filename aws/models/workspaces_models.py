from pydantic import BaseModel
from typing import List  ,Optional


class CreateWorkspaceRequest(BaseModel):
    #Todo - check multiple accounts

    # account_id: Optional[str]
    # role_name: Optional[str]

    directory_id: str
    user_name: str
    bundle_id: str


class CreateWorkspaceResponse(BaseModel):
    created_workspace_id: str