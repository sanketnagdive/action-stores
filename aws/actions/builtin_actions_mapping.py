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
    
    def mylist_buckets(params):
        return s3.list_buckets(**params)
    action_store.register_action('s3.ListBuckets', mylist_buckets)
    
    def mylist_objects(params):
        return s3.list_objects(**params)
    action_store.register_action('s3.ListObjects', mylist_objects)
    
    def mycopy_object(params):
        return s3.copy_object(**params)
    action_store.register_action('s3.CopyObject', mycopy_object)
    
    def mydescribe_repositories(params):
        return ecr.describe_repositories(**params)
    action_store.register_action('ecr.DescribeRepositories', mydescribe_repositories)
    
    def mydescribe_images(params):
        return ecr.describe_images(**params)
    action_store.register_action('ecr.DescribeImages', mydescribe_images)
    
    def mylist_images(params):
        return ecr.list_images(**params)
    action_store.register_action('ecr.ListImages', mylist_images)
    
    def mylist_clusters(params):
        return ecs.list_clusters(**params)
    action_store.register_action('ecs.ListClusters', mylist_clusters)
    
    def mylist_services(params):
        return ecs.list_services(**params)
    action_store.register_action('ecs.ListServices', mylist_services)
    
    def myupdate_service(params):
        return ecs.update_service(**params)
    action_store.register_action('ecs.UpdateService', myupdate_service)
    
    def mydescribe_clusters(params):
        return ecs.describe_clusters(**params)
    action_store.register_action('ecs.DescribeClusters', mydescribe_clusters)
    
    def mylist_task_definitions(params):
        return ecs.list_task_definitions(**params)
    action_store.register_action('ecs.ListTaskDefinitions', mylist_task_definitions)
    
    def mydescribe_task_definition(params):
        return ecs.describe_task_definition(**params)
    action_store.register_action('ecs.DescribeTaskDefinition', mydescribe_task_definition)
    
    def myget_caller_identity(params):
        return sts.get_caller_identity(**params)
    action_store.register_action('sts.GetCallerIdentity', myget_caller_identity)
    
    def mylist_roles(params):
        return iam.list_roles(**params)
    action_store.register_action('iam.ListRoles', mylist_roles)
    
    def mylist_users(params):
        return iam.list_users(**params)
    action_store.register_action('iam.ListUsers', mylist_users)
    
    def mylist_groups(params):
        return iam.list_groups(**params)
    action_store.register_action('iam.ListGroups', mylist_groups)
    
    def mylist_policies(params):
        return iam.list_policies(**params)
    action_store.register_action('iam.ListPolicies', mylist_policies)
    
    def myattach_role_policy(params):
        return iam.attach_role_policy(**params)
    action_store.register_action('iam.AttachRolePolicy', myattach_role_policy)
    
    def myput_parameter(params):
        return ssm.put_parameter(**params)
    action_store.register_action('ssm.PutParameter', myput_parameter)
    
    def mylist_queues(params):
        return sqs.list_queues(**params)
    action_store.register_action('sqs.ListQueues', mylist_queues)
    
    def mysend_message(params):
        return sqs.send_message(**params)
    action_store.register_action('sqs.SendMessage', mysend_message)
    
    def mydescribe_instances(params):
        return ec2.describe_instances(**params)
    action_store.register_action('ec2.DescribeInstances', mydescribe_instances)
    
    def myterminate_instances(params):
        return ec2.terminate_instances(**params)
    action_store.register_action('ec2.TerminateInstances', myterminate_instances)
    
    def myreboot_instances(params):
        return ec2.reboot_instances(**params)
    action_store.register_action('ec2.RebootInstances', myreboot_instances)
    
    def myrun_instances(params):
        return ec2.run_instances(**params)
    action_store.register_action('ec2.RunInstances', myrun_instances)
    
    def mydescribe_instances(params):
        return ec2.describe_instances(**params)
    action_store.register_action('ec2.DescribeInstanceTypes', mydescribe_instances)
    
    def mydescribe_security_groups(params):
        return ec2.describe_security_groups(**params)
    action_store.register_action('ec2.DescribeSecurityGroups', mydescribe_security_groups)
    
    def mydescribe_images(params):
        return ec2.describe_images(**params)
    action_store.register_action('ec2.DescribeImages', mydescribe_images)
    
    def mydescribe_security_groups(params):
        return ec2.describe_security_groups(**params)
    action_store.register_action('ec2.DescribeSecurityGroupRules', mydescribe_security_groups)
    
     

register_some_actions(action_store)