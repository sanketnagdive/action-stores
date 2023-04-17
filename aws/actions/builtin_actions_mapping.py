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

def get_narrow_actions_map() -> Dict[str, Dict]:    
    endpoint_url=os.environ.get('LOCALSTACK_HOST')

    s3 = boto3.client('s3', endpoint_url=endpoint_url)
    ecr = boto3.client('ecr', endpoint_url=endpoint_url)
    ecs = boto3.client('ecs', endpoint_url=endpoint_url)
    sts = boto3.client('sts', endpoint_url=endpoint_url)
    iam = boto3.client('iam', endpoint_url=endpoint_url)
    ssm = boto3.client('ssm', endpoint_url=endpoint_url)
    sqs = boto3.client('sqs', endpoint_url=endpoint_url)
    ec2 = boto3.client('ec2', endpoint_url=endpoint_url)
    
    return {
        's3.ListBuckets':                       s3.list_buckets,
        's3.ListObjects':                       s3.list_objects,
        's3.CopyObject':                        s3.copy_object,
        
        'ecr.DescribeRepositories':             ecr.describe_repositories,
        'ecr.DescribeImages':                   ecr.describe_images,
        'ecr.ListImages':                       ecr.list_images,
        
        'ecs.ListClusters':                     ecs.list_clusters,
        'ecs.ListServices':                     ecs.list_services,
        'ecs.UpdateService':                    ecs.update_service,
        'ecs.DescribeClusters':                 ecs.describe_clusters,
        'ecs.ListTaskDefinitions':              ecs.list_task_definitions,
        'ecs.DescribeTaskDefinition':           ecs.describe_task_definition,
        
        'sts.GetCallerIdentity':                sts.get_caller_identity,
        
        'iam.ListRoles':                        iam.list_roles,
        'iam.ListUsers':                        iam.list_users,
        'iam.ListGroups':                       iam.list_groups,
        'iam.ListPolicies':                     iam.list_policies,
        'iam.AttachRolePolicy':                 iam.attach_role_policy,
        
        'ssm.PutParameter':                     ssm.put_parameter,
        
        'sqs.ListQueues':                       sqs.list_queues,
        'sqs.SendMessage':                      sqs.send_message,
        
        'ec2.DescribeInstances':                ec2.describe_instances,
        'ec2.TerminateInstances':               ec2.terminate_instances,
        'ec2.RebootInstances':                  ec2.reboot_instances,
        'ec2.RunInstances':                     ec2.run_instances,
        'ec2.DescribeInstanceTypes':            ec2.describe_instances,
        'ec2.DescribeSecurityGroups':           ec2.describe_security_groups,
        'ec2.DescribeImages':                   ec2.describe_images,
        'ec2.DescribeSecurityGroupRules':       ec2.describe_security_groups,
    }
    
def register_some_actions():
    for operation_name, method in get_narrow_actions_map().items():
        action_store.register_action(operation_name, method)

register_some_actions()