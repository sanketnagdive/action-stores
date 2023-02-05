import json
from typing import Any, Dict, List, Optional

import boto3
from . import action_store


@action_store.kubiya_action()
def ecs_list_clusters(input_stuff):
    """List all ECS clusters defined in the account."""

    resource = boto3.client(
        "ecs",
        aws_access_key_id=action_store.secrets.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=action_store.secrets.get("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=action_store.secrets.get("AWS_SESSION_TOKEN"),
        region_name="us-east-1",
    )
    clusters = resource.list_clusters()
    return clusters
