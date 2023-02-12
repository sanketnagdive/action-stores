"""recursively registers actions available in boto3"""
from functools import partial
from typing import Dict, List

import boto3
import botocore

from . import action_store

# Global wrapper for all AWS actions
def aws_wrapper(service: str, operation: str, params: dict = dict()):
    try:
        resource = boto3.client(
            service,
            aws_access_key_id=action_store.secrets.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=action_store.secrets.get("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=action_store.secrets.get("AWS_SESSION_TOKEN"),
        )
    except botocore.exceptions.UnknownServiceError:
        raise Exception(f"Unknown service: {service}")
    caller = getattr(resource, operation)
    if not caller or not callable(caller):
        raise Exception(f"Unknown command for {service}: {operation}")
    return caller(**params)


def get_service_list() -> List[str]:
    session = boto3.Session()
    print("Mapping available AWS services ..")
    return session.get_available_resources() + session.get_available_services()


def get_service_operations(service: str) -> Dict:
    cli = boto3.client(service)
    return {
        op_name: method_name
        for method_name, op_name in cli.meta.method_to_api_mapping.items()
    }


def get_actions_map() -> Dict[str, Dict]:
    return {service: get_service_operations(service) for service in get_service_list()}


def register_all_actions():
    services = get_actions_map()
    for service, operations in services.items():
        for operation_name, method_name in operations.items():
            actionname = f"{service}.{operation_name}"
            action = partial(aws_wrapper, service, method_name)
            action.__name__ = actionname
            action_store.kubiya_action()(action)


register_all_actions()
