from typing import List
from pydantic import BaseModel
import boto3
import logging as log
from . import action_store

class HealthRequest(BaseModel):
    pass

class HealthResponse(BaseModel):
    params: bool
    connection: bool
    errors: List[str]

@action_store.kubiya_action()
def health_check(_) -> HealthResponse:
    errs = []
    key = action_store.secrets.get("AWS_ACCESS_KEY_ID")
    region = action_store.secrets.get("AWS_DEFAULT_REGION")
    session = action_store.secrets.get("AWS_SESSION_TOKEN")
    secret = action_store.secrets.get("AWS_SECRET_ACCESS_KEY")
    
    valid_key = _param(key)
    valid_region = _param(region)
    valid_secret = _param(secret)
    valid_session = _param(session)
    
    if not valid_key:
        errs.append("AWS_ACCESS_KEY_ID is not set")
        
    if not valid_region:
        errs.append("AWS_DEFAULT_REGION is not set")
        
    if not valid_secret:
        errs.append("AWS_SECRET_ACCESS_KEY is not set")
    
    if not valid_session:
        errs.append("AWS_SESSION_TOKEN is not set")
        
    valid_conn= _conn(errs)
    valid_params = valid_key and valid_region and valid_secret and valid_session
    return HealthResponse(params=valid_params, connection=valid_conn, errors=errs)


def _conn(e: List[str]) -> bool:
    try:
        c = boto3.client(
            "ecs",
            aws_access_key_id=action_store.secrets.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=action_store.secrets.get("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=action_store.secrets.get("AWS_SESSION_TOKEN"),
            region_name=action_store.secrets.get("AWS_DEFAULT_REGION"),
        )
        return c.list_clusters().get("clusterArns") is not None
    except Exception as e:
        log.error("[error]", exception=str(e))
        e.append(f"faild to connect to aws: {str(e)}")
        return False


def _param(p: str) -> bool:
    return p is not None and p != ""