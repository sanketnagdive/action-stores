from ..models.workspaces_models import (
    # TerminateInstanceRequest,
    # TerminateInstanceResponse,
    CreateWorkspaceRequest,
    CreateWorkspaceResponse,
    # ListInstancesRequest,
    # ListInstancesResponse,
)

from ..main_store import store
from ..aws_wrapper import get_client,get_session


# @store.kubiya_action()
# def terminate_ec2_instance(request: TerminateInstanceRequest) -> TerminateInstanceResponse:
#     """
#     Terminates the specified EC2 instance.
#
#     Args:
#         request (TerminateInstanceRequest): The request containing the ID of the EC2 instance to terminate.
#
#     Returns:
#         TerminateInstanceResponse: The response containing a message indicating the termination of the instance.
#     """
#     ec2 = get_resource("ec2")
#     ec2.terminate_instances(InstanceIds=[request.instance_id])
#     message = f'Instance {request.instance_id} termination initiated.'
#     return TerminateInstanceResponse(message=message)


@store.kubiya_action()
def create_workspace(request: CreateWorkspaceRequest) -> CreateWorkspaceResponse:
    """
    Creates a new Workspace .

    Args:
        request (CreateWorkspaceRequest): The request containing the details of the workspace to create.

    Returns:
        CreateWorkspaceResponse: The response containing the details of the created workspace.
    """

    workspaces_l=[
        {
            'DirectoryId': request.directory_id,
            'UserName': request.user_name,
            'BundleId': request.bundle_id,
            'UserVolumeEncryptionEnabled': False,
            'RootVolumeEncryptionEnabled': False,
            'WorkspaceProperties': {
                'RunningMode': 'ALWAYS_ON',
                'RootVolumeSizeGib': 80,
                'UserVolumeSizeGib': 10,
                'ComputeTypeName': 'VALUE'}
        }
    ]

    if request.account_id is not None and request.role_name is not None:
        workspace = get_session("workspaces", request.account_id, request.role_name)
        response = workspace.create_workspaces(
            Workspaces=workspaces_l
        )
    else:
        workspace = get_client("workspaces")
        response = workspace.create_workspaces(
            Workspaces=workspaces_l
        )
    workspace_id = "workspace was created"
    return CreateWorkspaceResponse(created_workspace_id=workspace_id)


# @store.kubiya_action()
# def list_ec2_instances(request: ListInstancesRequest) -> ListInstancesResponse:
#     """
#     Lists EC2 instances based on the specified filters.
#
#     Args:
#         request (ListInstancesRequest): The request containing the filters.
#
#     Returns:
#         ListInstancesResponse: The response containing the list of instances.
#     """
#     ec2 = get_resource("ec2")
#     filters = []
#     if request.instance_ids:
#         filters.append({'Name': 'instance-id', 'Values': request.instance_ids})
#     if request.instance_types:
#         filters.append({'Name': 'instance-type', 'Values': request.instance_types})
#     # Add more filters as needed...
#     response = ec2.describe_instances(Filters=filters)
#     instances = []
#     for reservation in response["Reservations"]:
#         instances.extend(reservation["Instances"])
#     return ListInstancesResponse(instances=instances)
