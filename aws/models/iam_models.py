from pydantic import BaseModel
from typing import List


class CreateUserRequest(BaseModel):
    username: str


class CreateUserResponse(BaseModel):
    username: str
    arn: str


class DeleteUserRequest(BaseModel):
    username: str


class DeleteUserResponse(BaseModel):
    username: str


class ListUsersRequest(BaseModel):
    usernames: List[str] = None


class ListUsersResponse(BaseModel):
    users: List[dict]


class CreateAccessKeyRequest(BaseModel):
    username: str


class CreateAccessKeyResponse(BaseModel):
    username: str
    access_key_id: str
    secret_access_key: str


class ListAccessKeysRequest(BaseModel):
    username: str


class ListAccessKeysResponse(BaseModel):
    access_keys: List[dict]
