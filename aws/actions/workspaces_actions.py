from ..models.workspaces_models import (
    CreateWorkspaceRequest,
    CreateWorkspaceResponse,
    DescribeWorkspaceRequest,
    DescribeWorkspaceResponse,
)

from ..main_store import store
from ..aws_wrapper import get_client ,get_session



@store.kubiya_action()
def create_workspace(request: CreateWorkspaceRequest) -> CreateWorkspaceResponse:
    """
    Creates a new Workspace .

    Args:
        request (CreateWorkspaceRequest): The request containing the details of the workspace to create.

    Returns:
        CreateWorkspaceResponse: The response containing the details of the created workspace.
    """


    if request.account_id is not None and request.role_name is not None:
        workspace = get_session("workspaces", request.account_id, request.role_name)
    else:
        workspace = get_client("workspaces")

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

    response = workspace.create_workspaces(
        Workspaces=workspaces_l
    )

    workspaces = response['PendingRequests']

    workspaces_ids_list = [workspace['WorkspaceId'] for workspace in workspaces]

    return CreateWorkspaceResponse(workspaces_ids=workspaces_ids_list)


@store.kubiya_action()
def describe_workspaces(request: DescribeWorkspaceRequest) -> DescribeWorkspaceResponse:
    """
    Describes the specified Workspaces.

    Args:
        request (DescribeWorkspaceRequest): The request containing the details of the workspace to describe.

    Returns:
        DescribeWorkspaceResponse: The response containing the details of the described workspace.
    """
    if request.account_id is not None and request.role_name is not None:
        workspace = get_session("workspaces", request.account_id, request.role_name)
    else:
        workspace = get_client("workspaces")

    response = workspace.describe_workspaces(
        WorkspaceIds=[request.workspace_id]
    )
    return DescribeWorkspaceResponse(workspace_details=response['Workspaces'][0])
