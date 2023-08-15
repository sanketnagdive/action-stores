from ..models.rds_models import (
    ListRDSInstancesRequest,
    ListRDSInstancesResponse,
    DescribeRDSSnapshotsRequest,
    DescribeRDSSnapshotsResponse,
    CreateRDSInstanceRequest,
    CreateRDSInstanceResponse
)

from ..main_store import store
from ..aws_wrapper import get_client


@store.kubiya_action()
def list_rds_instances(request: ListRDSInstancesRequest) -> ListRDSInstancesResponse:
    """
    List RDS instances using Boto3.

    Args:
        request (ListRDSInstancesRequest): The request containing the instance names (optional).

    Returns:
        ListRDSInstancesResponse: The response containing the list of RDS instance names.
    """
    rds_client = get_client("rds")
    response = rds_client.describe_db_instances()
    instances = response.get("DBInstances", [])
    instance_names = [instance["DBInstanceIdentifier"] for instance in instances]

    if request.instance_names:
        instance_names = [name for name in instance_names if name in request.instance_names]

    return ListRDSInstancesResponse(instance_names=instance_names)


@store.kubiya_action()
def describe_rds_snapshots(request: DescribeRDSSnapshotsRequest) -> DescribeRDSSnapshotsResponse:
    """
    Describe RDS snapshots using Boto3.

    Args:
        request (DescribeRDSSnapshotsRequest): The request containing the snapshot IDs.

    Returns:
        DescribeRDSSnapshotsResponse: The response containing the details of the described RDS snapshots.
    """
    rds_client = get_client("rds")
    response = rds_client.describe_db_snapshots(DBSnapshotIdentifier=request.snapshot_ids)
    snapshots = response.get("DBSnapshots", [])
    return DescribeRDSSnapshotsResponse(snapshots=snapshots)


@store.kubiya_action()
def create_rds_instance(request: CreateRDSInstanceRequest) -> CreateRDSInstanceResponse:
    """
    Create an RDS instance using Boto3.

    Args:
        request (CreateRDSInstanceRequest): The request containing the details of the RDS instance to create.

    Returns:
        CreateRDSInstanceResponse: The response containing the details of the created RDS instance.
    """
    rds_client = get_client("rds")
    response = rds_client.create_db_instance(
        DBInstanceIdentifier=request.instance_identifier,
        DBInstanceClass=request.db_instance_class,
        Engine=request.engine,
        AllocatedStorage=request.allocated_storage,
        MasterUsername=request.master_username,
        MasterUserPassword=request.master_password,
        PubliclyAccessible=True,  # Adjust this as needed
    )
    return CreateRDSInstanceResponse(DBInstance=response["DBInstance"], ResponseMetadata=response["ResponseMetadata"])