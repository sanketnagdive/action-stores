import json

import boto3
import moto

from aws.main_store import SQS, action_store

# Test your handler here

# To disable testing, you can set the build_arg `TEST_ENABLED=false` on the CLI or in your stack.yml
# https://docs.openfaas.com/reference/yaml/#function-build-args-build-args


def _mock_secrets(store):
    boto_screts = {
        "AWS_ACCESS_KEY_ID": "secret-value",
        "AWS_SECRET_ACCESS_KEY": "secret-value",
        "AWS_SESSION_TOKEN": "secret-value",
        "AWS_DEFAULT_REGION": "us-east-1",
    }
    setattr(store, "secrets", boto_screts)


def test_get_available_subresources():
    # assert handle("input") == "input"
    # create sqs with moto
    _mock_secrets(action_store)
    mock_sqs = moto.mock_sqs()
    mock_sqs.start()
    # create sqs client
    input = SQS.parse_raw('{"queue_name": "test-queue"}')
    sqs = boto3.client("sqs", region_name="us-east-1")
    # create queue
    queue = sqs.create_queue(QueueName="test-queue")
    # get queue url
    queue_url = sqs.get_queue_url(QueueName="test-queue")["QueueUrl"]
    # send message
    sqs.send_message(QueueUrl=queue_url, MessageBody="test message")
    output = action_store.execute_action("get_available_subresources", input.dict())
    action_metadata = action_store._action_metadata["receive_sqs_messages"]
    assert action_metadata["category"] == "sqs"
    assert output["data"]["ApproximateNumberOfMessages"] == "1"


def test_list_queues():
    _mock_secrets(action_store)
    # fake a few queues
    mock_sqs = moto.mock_sqs()
    mock_sqs.start()
    # create sqs client
    sqs = boto3.client("sqs", region_name="us-east-1")
    # create queue
    queue = sqs.create_queue(QueueName="test-queue")
    # get queue url
    queue_url = sqs.get_queue_url(QueueName="test-queue")["QueueUrl"]
    # send message
    sqs.send_message(QueueUrl=queue_url, MessageBody="test message")
    output = action_store.execute_action("list_sqs_queues", {})
    assert output
    assert len(output) == 1
    action_metadata = action_store._action_metadata["receive_sqs_messages"]
    assert action_metadata["category"] == "sqs"
    assert output[0].startswith("https://queue.amazonaws.com/")


def test_receive_messages():
    _mock_secrets(action_store)
    mock_sqs = moto.mock_sqs()
    mock_sqs.start()
    # create sqs client
    input = SQS.parse_raw('{"queue_name": "test-queue"}')
    sqs = boto3.client("sqs", region_name="us-east-1")
    # create queue
    queue = sqs.create_queue(QueueName="test-queue")
    # get queue url
    queue_url = sqs.get_queue_url(QueueName="test-queue")["QueueUrl"]
    # send message
    sqs.send_message(QueueUrl=queue_url, MessageBody="test message")
    output = action_store.execute_action("receive_sqs_messages", input.dict())
    action_metadata = action_store._action_metadata["receive_sqs_messages"]
    assert action_metadata["category"] == "sqs"
    assert output


def test_add_single_message_to_queue():
    _mock_secrets(action_store)
    mock_sqs = moto.mock_sqs()
    mock_sqs.start()
    # create sqs client
    input = SQS.parse_raw('{"queue_name": "test-queue"}')
    sqs = boto3.client("sqs", region_name="us-east-1")
    # create queue
    queue = sqs.create_queue(QueueName="test-queue")
    # get queue url
    queue_url = sqs.get_queue_url(QueueName="test-queue")["QueueUrl"]
    # # send message
    sqs.send_message(QueueUrl=queue_url, MessageBody="test message")
    output = action_store.execute_action("receive_sqs_messages", input.dict())
    assert output
    action_metadata = action_store._action_metadata["receive_sqs_messages"]
    assert action_metadata["category"] == "sqs"

    # output = action_store.execute_action("add_single_message_to_queue", {"queue_name": "test-queue", "message": output[0].__dict__)
