import boto3
import logging as log
from . import action_store

def health_check():
    key = action_store.secrets.get("AWS_ACCESS_KEY_ID")
    region = action_store.secrets.get("AWS_DEFAULT_REGION")
    session = action_store.secrets.get("AWS_SESSION_TOKEN")
    secret = action_store.secrets.get("AWS_SECRET_ACCESS_KEY")
    
    return _param(key) & _param(secret) & _param(region) & _param(session) & _conn()


def _conn() -> bool:
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
        return False


def _param(p: str) -> bool:
    return p is not None & p != ""