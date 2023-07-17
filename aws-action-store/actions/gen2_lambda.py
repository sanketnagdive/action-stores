import boto3
from pydantic import BaseModel
from typing import List, Optional, Literal
from . import store, KubiyaInputBaseModel, EmptyArgType, EmptyArg


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


class EC2Instance(BaseModel):
    """ Model to represent EC2 Instance configurations """
    instance_type: Literal['t2.micro', 't2.small', 't2.medium',
    't3.micro', 't3.small', 't3.medium',
    'm5.large', 'm5.xlarge', 'm5.2xlarge', 'm5.4xlarge']
    purpose: Literal['web_server', 'database', 'processing', 'storage',
    'api_server', 'cache', 'backup', 'dev_test', 'analytics', 'log_processing']
    external_facing: bool


class EC2SecurityGroup(BaseModel):
    GroupName: str
    GroupId: str


class EC2InstanceDetails(BaseModel):
    instance_id: str
    instance_type: str
    security_groups: List[EC2SecurityGroup]
    public_ip_address: Optional[str]
    private_ip_address: str
    state: str


InstanceState = Literal["pending", "running", "shutting-down", "terminated", "stopping", "stopped"]


class Instance(BaseModel):
    instance_id: str
    instance_type: str
    state: InstanceState


class EC2Filter(BaseModel):
    state: InstanceState


@store.kubiya_action()
def list_ec2_instances(filter_instances: EC2Filter) -> List[Instance]:
    """
    Lists EC2 instances based on their state.

    Args:
        filter_instances (EC2Filter): The filter to apply.

    Returns:
        A list of instances in the specified state.
    """
    ec2 = get_resource("ec2")

    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': [filter_instances.state]
            },
        ],
    )

    instances = []
    for reservation in response["Reservations"]:
        for instance_info in reservation["Instances"]:
            instance = Instance(
                instance_id=instance_info["InstanceId"],
                instance_type=instance_info["InstanceType"],
                state=instance_info["State"]["Name"],
            )
            instances.append(instance)

    return instances


@store.kubiya_action()
def create_ec2_instance(data: EC2Instance) -> EC2InstanceDetails:
    """
    Creates an EC2 instance with the specified configuration.

    Args:
        data (EC2Instance): The configuration data for the EC2 instance.

    Returns:
        The details of the created EC2 instance.
    """
    ec2 = get_resource("ec2")
    instance = ec2.run_instances(
        ImageId='ami-0fb2f0b847d44d4f0',  # Amazon Linux 2 AMI (HVM)
        MinCount=1,
        MaxCount=1,
        InstanceType=data.instance_type,
        # NetworkInterfaces=[{'AssociatePublicIpAddress': data.external_facing}],
    )

    instance_info = instance['Instances'][0]
    instance_details = EC2InstanceDetails(
        instance_id=instance_info['InstanceId'],
        instance_type=instance_info['InstanceType'],
        security_groups=[EC2SecurityGroup(GroupName=sg['GroupName'], GroupId=sg['GroupId']) for sg in
                         instance_info['SecurityGroups']],
        public_ip_address=instance_info.get('PublicIpAddress'),
        private_ip_address=instance_info['PrivateIpAddress'],
        state=instance_info['State']['Name'],
    )

    return instance_details


@store.kubiya_action()
def terminate_ec2_instance(instance_id: str):
    """
    Terminates the specified EC2 instance.

    Args:
        instance_id (str): The ID of the EC2 instance to terminate.

    Returns:
        A message indicating the termination of the instance.
    """
    ec2 = get_resource("ec2")
    ec2.terminate_instances(InstanceIds=[instance_id])
    return f'Instance {instance_id} termination initiated.'


class S3CopyData(BaseModel):
    """ Model to represent S3 file copy configuration """
    # Always use kubiya-demo-1 as source bucket
    source_bucket: Literal[
        'kubiya-demo-1',
        'kubiya-demo-2',
    ]
    destination_bucket: Literal[
        'kubiya-demo-1',
        'kubiya-demo-2',
    ]
    file_name: Literal['Demodemo', 'testing', 'copied_with_jq_and_actions']


@store.kubiya_action()
def copy_s3_file(data: S3CopyData):
    """
    Copies a file from one S3 bucket to another.

    Args:
        data (S3CopyData): The configuration data for the S3 copy operation.

    Returns:
        A message indicating the completion of the copy operation.
    """
    s3 = get_resource('s3')
    copy_source = {
        'Bucket': data.source_bucket,
        'Key': data.file_name
    }
    s3.copy(copy_source, data.destination_bucket, data.file_name)
    return f'File {data.file_name} copied from {data.source_bucket} to {data.destination_bucket}.'


@store.kubiya_action()
def get_repository_images(repository_name: str):
    """
    Retrieves images for the specified ECR repository.

    Args:
        repository_name (str): The name of the ECR repository.

    Returns:
        A list of image details in the specified ECR repository.
    """
    ecr = get_resource('ecr')
    response = ecr.describe_images(repositoryName=repository_name)
    return response['imageDetails']


@store.kubiya_action()
def get_repositories():
    """
    Retrieves all ECR repositories.

    Returns:
        A list of all ECR repository details.
    """
    ecr = get_resource('ecr')
    response = ecr.describe_repositories()
    return response['repositories']
