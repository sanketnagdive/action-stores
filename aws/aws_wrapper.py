import os
import boto3
from .main_store import store


def get_resource(service_name: str):
    """
    Returns a boto3 resource for a specific service.

    Args:
        service_name (str): The name of the AWS service.

    Returns:
        A boto3 resource for the specified service.
    """
    region = os.getenv("AWS_REGION", "eu-west-1")
    return boto3.resource(service_name,
                          aws_access_key_id="dummy",
                          aws_secret_access_key="dummy",
                          endpoint_url="http://172.18.0.2:31566",
                          region_name=region
                          )


def get_client(service_name: str):
    """
    Returns a boto3 client for a specific service.

    Args:
        service_name (str): The name of the AWS service.

    Returns:
        A boto3 client for the specified service.
    """
    region = os.getenv("AWS_REGION", "eu-west-1")
    return boto3.client(service_name,
                        aws_access_key_id="dummy",
                        aws_secret_access_key="dummy",
                        endpoint_url="http://172.18.0.2:31566",
                        region_name=region
                        )


def get_session(service_name: str):
    """
    Returns a boto3 session configured for LocalStack.
    """

    # Configure LocalStack S3 endpoint URL
    localstack_s3_endpoint = "http://172.18.0.2:31566"  # Adjust the URL based on your LocalStack setup

    # Assume role in the target account (simulating for LocalStack)
    assumed_role = {
        'Credentials': {
            'AccessKeyId': 'dummy',
            'SecretAccessKey': 'dummy',
            'SessionToken': 'dummy'
        }
    }

    # Create a session with the assumed role credentials and LocalStack endpoint
    region = os.getenv("AWS_REGION", "eu-west-1")
    session = boto3.Session(
        aws_access_key_id=assumed_role['Credentials']['AccessKeyId'],
        aws_secret_access_key=assumed_role['Credentials']['SecretAccessKey'],
        aws_session_token=assumed_role['Credentials']['SessionToken'],
        region_name=region,
        endpoint_url=localstack_s3_endpoint  # Use LocalStack S3 endpoint
    )

    # Create the client using the session
    client = session.client(service_name)

    return client