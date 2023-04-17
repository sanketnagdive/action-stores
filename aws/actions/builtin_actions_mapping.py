import logging
from pydantic import BaseModel
import boto3
import botocore
from functools import partial
from typing import Optional, List, Dict
import os
from . import actionstore as action_store

logging.basicConfig(level=logging.INFO)

# The action store definition is declared in the __init__.py file
# This is the main file that is executed when the action store is deployed


# This is a helper set of functions that will be used to register all the AWS actions
# in the action store. This is a bit of a hack, but it works for now. The idea is to
# dynamically register all the AWS actions in the action store. This is done by
# iterating over all the AWS services and then iterating over all the operations
# for each service. The operations are then registered in the action store.

# The AWS actions are registered in the action store with the following naming
# convention: <service>.<operation>. For example, the action to list all the
# EC2 instances is registered as ec2.describe_instances. The action store
# will then be able to execute this action by calling the ec2.describe_instances
# action.

# LocalStack is a mock AWS service that can be used for local development
# Port 4566 is the default port for LocalStack
USE_LOCALSTACK = os.environ.get("LOCALSTACK_HOST")

# Region is set to us-east-1 by default. This is because the AWS SDK will
# automatically use the region from the environment variable AWS_DEFAULT_REGION
if not os.environ.get("AWS_DEFAULT_REGION"):
    logging.info("AWS_DEFAULT_REGION not set, defaulting to us-east-1")
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


# The AWS credentials are set from the environment variables
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY and AWS_SESSION_TOKEN. These
# environment variables are set by the runner when the action store is executed.
# If LocalStack is used, the AWS credentials are not needed
if USE_LOCALSTACK:
    logging.info("Using LocalStack - no AWS credentials needed")
    logging.info(f"LocalStack hostname: {os.environ.get('LOCALSTACK_HOSTNAME')}")

def aws_wrapper(service: str, operation: str, params:dict=dict()):
    try:
        # If LocalStack is used, the endpoint URL is set to the LocalStack host
        if USE_LOCALSTACK:
            resource = boto3.client(service,
                endpoint_url=f"{os.environ.get('LOCALSTACK_HOST')}")
        else:
            if not os.environ.get('AWS_ACCESS_KEY_ID'):
                logging.warning("AWS SDK credentials not set in the environment - this may cause errors connecting to AWS")
            resource = boto3.client(service,
                aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
                aws_session_token=os.environ.get('AWS_SESSION_TOKEN'))
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
    return {
        service: get_service_operations(service)
        for service in get_service_list()
    }


def register_all_actions():
    services = get_actions_map()
    for service, operations in services.items():
        for operation_name, method_name in operations.items():
            actionname = f"{service}.{operation_name}"
            action = partial(aws_wrapper, service, method_name)
            action_store.register_action(actionname, action)

    
def register_some_actions(action_store):
    endpoint_url=os.environ.get('LOCALSTACK_HOST')

    s3 = boto3.client('s3', endpoint_url=endpoint_url)
    ecr = boto3.client('ecr', endpoint_url=endpoint_url)
    ecs = boto3.client('ecs', endpoint_url=endpoint_url)
    sts = boto3.client('sts', endpoint_url=endpoint_url)
    iam = boto3.client('iam', endpoint_url=endpoint_url)
    ssm = boto3.client('ssm', endpoint_url=endpoint_url)
    sqs = boto3.client('sqs', endpoint_url=endpoint_url)
    ec2 = boto3.client('ec2', endpoint_url=endpoint_url)
    
    action_store.register_action('s3.ListBuckets', lambda x: s3.list_buckets(**{"input": x}))
    action_store.register_action('s3.ListObjects', lambda x: s3.list_objects(**{"input": x}))
    action_store.register_action('s3.CopyObject', lambda x: s3.copy_object(**{"input": x}))
    action_store.register_action('ecr.DescribeRepositories', lambda x: ecr.describe_repositories(**{"input": x}))
    action_store.register_action('ecr.DescribeImages', lambda x: ecr.describe_images(**{"input": x}))
    action_store.register_action('ecr.ListImages', lambda x: ecr.list_images(**{"input": x}))
    action_store.register_action('ecs.ListClusters', lambda x: ecs.list_clusters(**{"input": x}))
    action_store.register_action('ecs.ListServices', lambda x: ecs.list_services(**{"input": x}))
    action_store.register_action('ecs.UpdateService', lambda x: ecs.update_service(**{"input": x}))
    action_store.register_action('ecs.DescribeClusters', lambda x: ecs.describe_clusters(**{"input": x}))
    action_store.register_action('ecs.ListTaskDefinitions', lambda x: ecs.list_task_definitions(**{"input": x}))
    action_store.register_action('ecs.DescribeTaskDefinition', lambda x: ecs.describe_task_definition(**{"input": x}))
    action_store.register_action('sts.GetCallerIdentity', lambda x: sts.get_caller_identity(**{"input": x}))
    action_store.register_action('iam.ListRoles', lambda x: iam.list_roles(**{"input": x}))
    action_store.register_action('iam.ListUsers', lambda x: iam.list_users(**{"input": x}))
    action_store.register_action('iam.ListGroups', lambda x: iam.list_groups(**{"input": x}))
    action_store.register_action('iam.ListPolicies', lambda x: iam.list_policies(**{"input": x}))
    action_store.register_action('iam.AttachRolePolicy', lambda x: iam.attach_role_policy(**{"input": x}))
    action_store.register_action('ssm.PutParameter', lambda x: ssm.put_parameter(**{"input": x}))
    action_store.register_action('sqs.ListQueues', lambda x: sqs.list_queues(**{"input": x}))
    action_store.register_action('sqs.SendMessage', lambda x: sqs.send_message(**{"input": x}))
    action_store.register_action('ec2.DescribeInstances', lambda x: ec2.describe_instances(**{"input": x}))
    action_store.register_action('ec2.TerminateInstances', lambda x: ec2.terminate_instances(**{"input": x}))
    action_store.register_action('ec2.RebootInstances', lambda x: ec2.reboot_instances(**{"input": x}))
    action_store.register_action('ec2.RunInstances', lambda x: ec2.run_instances(**{"input": x}))
    action_store.register_action('ec2.DescribeInstanceTypes', lambda x: ec2.describe_instances(**{"input": x}))
    action_store.register_action('ec2.DescribeSecurityGroups', lambda x: ec2.describe_security_groups(**{"input": x}))
    action_store.register_action('ec2.DescribeImages', lambda x: ec2.describe_images(**{"input": x}))
    action_store.register_action('ec2.DescribeSecurityGroupRules', lambda x: ec2.describe_security_groups(**{"input": x}))
     

register_some_actions(action_store)