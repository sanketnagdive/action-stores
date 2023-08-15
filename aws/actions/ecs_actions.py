from ..models.ecs_models import (
    RegisterTaskDefinitionRequest,
    RegisterTaskDefinitionResponse,
    DescribeTaskDefinitionRequest,
    DescribeTaskDefinitionResponse,
    ListTaskDefinitionsRequest,
    ListTaskDefinitionsResponse,
    DescribeECSClustersRequest,
    DescribeECSClustersResponse,
    ListECSServicesRequest,
    ListECSServicesResponse,
    CreateECSClusterRequest,
    CreateECSClusterResponse,
    ListECSClustersRequest,
    ListECSClustersResponse
)

from ..main_store import store
from ..aws_wrapper import get_client, get_client


@store.kubiya_action()
def register_task_definition(request: RegisterTaskDefinitionRequest) -> RegisterTaskDefinitionResponse:
    """
    Registers a new task definition in ECS.

    Args:
        request (RegisterTaskDefinitionRequest): The request containing the details of the task definition.

    Returns:
        RegisterTaskDefinitionResponse: The response containing the details of the registered task definition.
    """
    ecs = get_client("ecs")
    response = ecs.register_task_definition(**request.dict(exclude_none=True))
    task_definition = response["taskDefinition"]
    return RegisterTaskDefinitionResponse(task_definition=task_definition)


@store.kubiya_action()
def describe_task_definition(request: DescribeTaskDefinitionRequest) -> DescribeTaskDefinitionResponse:
    """
    Describes a task definition in ECS.

    Args:
        request (DescribeTaskDefinitionRequest): The request containing the ARN of the task definition.

    Returns:
        DescribeTaskDefinitionResponse: The response containing the details of the task definition.
    """
    ecs = get_client("ecs")
    response = ecs.describe_task_definition(taskDefinition=request.task_definition_arn)
    task_definition = response["taskDefinition"]
    return DescribeTaskDefinitionResponse(task_definition=task_definition)


# @store.kubiya_action()
# def list_task_definitions(request: ListTaskDefinitionsRequest) -> ListTaskDefinitionsResponse:
#     """
#     Lists task definitions in ECS based on the specified filters.

#     Args:
#         request (ListTaskDefinitionsRequest): The request containing the filters.

#     Returns:
#         ListTaskDefinitionsResponse: The response containing the list of task definitions.
#     """
#     ecs = get_client("ecs")
#     response = ecs.list_task_definitions(
#         familyPrefix=request.family_prefix,
#         status=request.status,
#         sort=request.sort,
#         maxResults=request.max_results,
#         nextToken=request.next_token,
#     )
#     task_definitions = response["taskDefinitionArns"]
#     return ListTaskDefinitionsResponse(task_definitions=task_definitions)

@store.kubiya_action()
def list_task_definitions(request: ListTaskDefinitionsRequest) -> ListTaskDefinitionsResponse:
    """
    List ECS task definitions based on filters using Boto3.

    Args:
        request (ListTaskDefinitionsRequest): The request containing the filters.

    Returns:
        ListTaskDefinitionsResponse: The response containing the list of task definition ARNs.
    """
    ecs_client = get_client("ecs")
    filters = []

    if request.family_prefix:
        filters.append({"name": "family-prefix", "values": [request.family_prefix]})

    if request.status:
        filters.append({"name": "status", "values": [request.status]})

    response = ecs_client.list_task_definitions(
        familyPrefix=request.family_prefix,
        status=request.status,
        maxResults=request.max_results,
        nextToken=request.next_token,
    )

    task_definition_arns = response.get("taskDefinitionArns", [])
    next_token = response.get("nextToken")

    return ListTaskDefinitionsResponse(
        task_definition_arns=task_definition_arns,
        next_token=next_token,
    )

@store.kubiya_action()
def describe_ecs_clusters(request: DescribeECSClustersRequest) -> DescribeECSClustersResponse:
    """
    Describe ECS clusters using Boto3.

    Args:
        request (DescribeECSClustersRequest): The request containing the cluster names (optional).

    Returns:
        DescribeECSClustersResponse: The response containing the list of ECS clusters.
    """
    ecs_client = get_client("ecs")
    response = ecs_client.describe_clusters(clusterNames=request.cluster_names)
    clusters = response.get("clusters", [])
    return DescribeECSClustersResponse(clusters=clusters)


@store.kubiya_action()
def list_ecs_services(request: ListECSServicesRequest) -> ListECSServicesResponse:
    """
    List ECS services within a specific cluster using Boto3.

    Args:
        request (ListECSServicesRequest): The request containing the cluster name and service names (optional).

    Returns:
        ListECSServicesResponse: The response containing the list of ECS services.
    """
    ecs_client = get_client("ecs")
    response = ecs_client.list_services(cluster=request.cluster_name)
    services = response.get("serviceArns", [])
    return ListECSServicesResponse(services=services)


@store.kubiya_action()
def create_ecs_cluster(request: CreateECSClusterRequest) -> CreateECSClusterResponse:
    """
    Create an ECS cluster using Boto3.

    Args:
        request (CreateECSClusterRequest): The request containing the cluster name.

    Returns:
        CreateECSClusterResponse: The response containing the ARN of the created ECS cluster.
    """
    ecs_client = get_client("ecs")
    response = ecs_client.create_cluster(clusterName=request.cluster_name)
    cluster_arn = response["cluster"]["clusterArn"]
    return CreateECSClusterResponse(cluster_arn=cluster_arn)


@store.kubiya_action()
def list_ecs_clusters(request: ListECSClustersRequest) -> ListECSClustersResponse:
    """
    List ECS clusters using Boto3.

    Args:
        request (ListECSClustersRequest): The request containing the filters.

    Returns:
        ListECSClustersResponse: The response containing the list of ECS clusters.
    """
    ecs_client = get_client("ecs")
    response = ecs_client.list_clusters()
    cluster_arns = response.get("clusterArns", [])
    return ListECSClustersResponse(cluster_arns=cluster_arns)