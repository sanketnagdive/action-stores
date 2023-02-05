import json
from typing import List, Optional

import boto3
from pydantic import BaseModel

from . import action_store

class SQS(BaseModel):
    """follows model with attributes of sqs queue for boto3"""

    queue_name: str
    messages: Optional[List] = None


@action_store.kubiya_action()
def get_available_subresources(sqs: SQS):
    """returns list of available subresources for queue"""
    try:
        resource = boto3.resource(
            "sqs",
            aws_access_key_id=action_store.secrets.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=action_store.secrets.get("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=action_store.secrets.get("AWS_SESSION_TOKEN"),
            region_name=action_store.secrets.get("AWS_DEFAULT_REGION"),
        )
        queue = resource.get_queue_by_name(QueueName=sqs.queue_name)
        return {"data": queue.attributes}
    except boto3.exceptions.botocore.exceptions.ClientError as e:
        return {"error": e.response["Error"]["Message"]}


@action_store.kubiya_action()
def receive_sqs_messages(sqs: SQS):
    """returns list of available subresources for queue"""
    try:
        resource = boto3.resource(
            "sqs",
            aws_access_key_id=action_store.secrets.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=action_store.secrets.get("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=action_store.secrets.get("AWS_SESSION_TOKEN"),
            region_name=action_store.secrets.get("AWS_DEFAULT_REGION"),
        )
        queue = resource.get_queue_by_name(QueueName=sqs.queue_name)
        messages = queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=4)
        json_messages = []
        for message in messages:
            message_dict = message.attributes or {}
            message_dict["message_id"] = message.message_id
            message_dict["body"] = message.body
            json_messages.append(json.dumps(message_dict))
        return json_messages
    except boto3.exceptions.botocore.exceptions.ClientError as e:
        return e.response


@action_store.kubiya_action()
def return_sqs_messages_to_queue(sqs: SQS):
    """returns list of available subresources for queue"""
    try:
        message_id = sqs.message_id
        resource = boto3.resource(
            "sqs",
            aws_access_key_id=action_store.secrets.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=action_store.secrets.get("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=action_store.secrets.get("AWS_SESSION_TOKEN"),
            region_name=action_store.secrets.get("AWS_DEFAULT_REGION"),
        )
        client = boto3.client(
            "sqs",
            aws_access_key_id=action_store.secrets.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=action_store.secrets.get("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=action_store.secrets.get("AWS_SESSION_TOKEN"),
            region_name=action_store.secrets.get("AWS_DEFAULT_REGION"),
        )
        queue = resource.get_queue_by_name(QueueName=sqs.queue_name)
        # Get the queue URL
        queue_url = client.get_queue_url(QueueName=sqs.queue_name)["QueueUrl"]
        response = client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=["All"],
            MaxNumberOfMessages=1,
            MessageAttributeNames=["All"],
            WaitTimeSeconds=0,
        )
        if "Messages" in response:
            message = response["Messages"][0]
            if message["MessageId"] == message_id:
                receipt_handle = message["ReceiptHandle"]
                # Delete the message
                sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
                return "OK"
            else:
                return "Message ID not found"
        else:
            return "No messages in the queue"
        return "OK"
    except boto3.exceptions.botocore.exceptions.ClientError as e:
        return e.response


@action_store.kubiya_action()
def list_sqs_queues(args):
    """returns list of available subresources for queue"""
    try:
        resource = boto3.resource(
            "sqs",
            aws_access_key_id=action_store.secrets.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=action_store.secrets.get("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=action_store.secrets.get("AWS_SESSION_TOKEN"),
            region_name=action_store.secrets.get("AWS_DEFAULT_REGION"),
        )
        # return the queue names
        queues = resource.queues.all()
        return [queue.url for queue in queues]

    except boto3.exceptions.botocore.exceptions.ClientError as e:
        return e.response
