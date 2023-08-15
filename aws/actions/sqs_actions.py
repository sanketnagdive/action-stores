from ..models.sqs_models import (
    CreateSQSQueueRequest,
    CreateSQSQueueResponse,
    ListSQSQueuesRequest,
    ListSQSQueuesResponse,
    GetSQSQueueAttributesRequest,
    GetSQSQueueAttributesResponse,


)

from ..main_store import store
from ..aws_wrapper import get_client


@store.kubiya_action()
def create_sqs_queue(request: CreateSQSQueueRequest) -> CreateSQSQueueResponse:
    """
    Create an SQS queue using Boto3.

    Args:
        request (CreateSQSQueueRequest): The request containing the queue name.

    Returns:
        CreateSQSQueueResponse: The response containing the URL of the created SQS queue.
    """
    sqs_client = get_client("sqs")
    response = sqs_client.create_queue(QueueName=request.queue_name)
    queue_url = response.get("QueueUrl", "")
    return CreateSQSQueueResponse(queue_url=queue_url)


@store.kubiya_action()
def list_sqs_queues(request: ListSQSQueuesRequest) -> ListSQSQueuesResponse:
    """
    List SQS queues using Boto3.

    Args:
        request (ListSQSQueuesRequest): The request.

    Returns:
        ListSQSQueuesResponse: The response containing the list of SQS queue URLs.
    """
    sqs_client = get_client("sqs")
    response = sqs_client.list_queues()
    queue_urls = response.get("QueueUrls", [])
    return ListSQSQueuesResponse(queue_urls=queue_urls)


@store.kubiya_action()
def get_sqs_queue_attributes(request: GetSQSQueueAttributesRequest) -> GetSQSQueueAttributesResponse:
    """
    Get attributes of an SQS queue using Boto3.

    Args:
        request (GetSQSQueueAttributesRequest): The request containing the queue URL.

    Returns:
        GetSQSQueueAttributesResponse: The response containing the attributes of the SQS queue.
    """
    sqs_client = get_client("sqs")
    response = sqs_client.get_queue_attributes(QueueUrl=request.queue_url, AttributeNames=["All"])
    attributes = response.get("Attributes", {})
    return GetSQSQueueAttributesResponse(attributes=attributes)