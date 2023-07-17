import boto3
from .main_store import store


def get_resource(service_name: str):
    """
    Returns a boto3 client for a specific service.

    Args:
        service_name (str): The name of the AWS service.

    Returns:
        A boto3 client for the specified service.
    """
    return boto3.client(service_name,
                        aws_access_key_id=store.secrets["AWS_ACCESS_KEY_ID"],
                        aws_secret_access_key=store.secrets["AWS_SECRET_ACCESS_KEY"],
                        aws_session_token=store.secrets["AWS_SESSION_TOKEN"],
                        region_name="eu-west-1"
                        )


def get_client(service_name: str):
    """
    Returns a boto3 client for a specific service.

    Args:
        service_name (str): The name of the AWS service.

    Returns:
        A boto3 client for the specified service.
    """
    return boto3.client(service_name,
                        aws_access_key_id=store.secrets["AWS_ACCESS_KEY_ID"],
                        aws_secret_access_key=store.secrets["AWS_SECRET_ACCESS_KEY"],
                        aws_session_token=store.secrets["AWS_SESSION_TOKEN"],
                        region_name="eu-west-1"
                        )
