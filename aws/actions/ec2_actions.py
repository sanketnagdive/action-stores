from ..models.ec2_models import (
    CreateInstanceRequest,
    CreateInstanceResponse,
    ListInstancesRequest,
    ListInstancesResponse,
    RebootInstanceRequest,
    RebootInstanceResponse,
    DescribeSecurityGroupsRequest,
    DescribeSecurityGroupsResponse
)

from ..main_store import store
from ..aws_wrapper import get_client


@store.kubiya_action()
def create_ec2_instance(request: CreateInstanceRequest) -> CreateInstanceResponse:
    """
    Creates a new EC2 instance.

    Args:
        request (CreateInstanceRequest): The request containing the details of the instance to create.

    Returns:
        CreateInstanceResponse: The response containing the details of the created instance.
    """
    ec2 = get_client("ec2")
    response = ec2.run_instances(
        ImageId=request.image_id,
        InstanceType=request.instance_type,
        MinCount=request.min_count,
        MaxCount=request.max_count
    )
    instance_id = response["Instances"][0]["InstanceId"]
    return CreateInstanceResponse(instance_id=instance_id)


@store.kubiya_action()
def list_ec2_instances(request: ListInstancesRequest) -> ListInstancesResponse:
    """
    Lists EC2 instances based on the specified filters.

    Args:
        request (ListInstancesRequest): The request containing the filters.

    Returns:
        ListInstancesResponse: The response containing the list of instances.
    """
    ec2 = get_client("ec2")
    filters = []
    # if request.instance_ids:
    #     filters.append({'Name': 'instance-id', 'Values': request.instance_ids})
    # if request.instance_types:
    #     filters.append({'Name': 'instance-type', 'Values': request.instance_types})
    # Add more filters as needed...
    response = ec2.describe_instances(Filters=filters)
    instances = []
    for reservation in response["Reservations"]:
        instances.extend(reservation["Instances"])
    return ListInstancesResponse(instances=instances)


@store.kubiya_action()
def reboot_ec2_instance(request: RebootInstanceRequest) -> RebootInstanceResponse:
    """
    Reboot a specific EC2 instance using Boto3.

    Args:
        request (RebootInstanceRequest): The request containing the instance ID.

    Returns:
        RebootInstanceResponse: The response indicating the success message.
    """
    ec2_client = get_client("ec2")
    ec2_client.reboot_instances(InstanceIds=[request.instance_id])
    return RebootInstanceResponse(message=f"Instance {request.instance_id} rebooted successfully.")


@store.kubiya_action()
def describe_security_groups(request: DescribeSecurityGroupsRequest) -> DescribeSecurityGroupsResponse:
    """
    Describe security groups associated with a specific EC2 instance using Boto3.

    Args:
        request (DescribeSecurityGroupsRequest): The request containing the instance ID.

    Returns:
        DescribeSecurityGroupsResponse: The response containing the list of security groups.
    """
    ec2_client = get_client("ec2")
    response = ec2_client.describe_instances(InstanceIds=[request.instance_id])
    security_groups = response["Reservations"][0]["Instances"][0]["SecurityGroups"]
    return DescribeSecurityGroupsResponse(security_groups=security_groups)