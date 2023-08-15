from ..models.s3_models import (
    CreateS3BucketRequest,
    ListS3BucketsRequest
)

from ..main_store import store
from ..aws_wrapper import get_client


@store.kubiya_action()
def create_s3_bucket(request: CreateS3BucketRequest):
    s3_client = get_client("s3")
    create_bucket_config = {"LocationConstraint": s3_client.meta.region_name}
    response = s3_client.create_bucket(
        Bucket=request.bucket_name,
        CreateBucketConfiguration=create_bucket_config
    )
    return response

@store.kubiya_action()
def list_s3_buckets(request: ListS3BucketsRequest):
    """
    List all S3 buckets using Boto3 and LocalStack.
    """
    s3_client = get_client("s3")
    response = s3_client.list_buckets()
    bucket_names = [bucket['Name'] for bucket in response.get('Buckets', [])]
    return bucket_names


# @store.kubiya_action()
# def list_s3_objects(input_data: S3ListObjectsInput) -> S3ListObjectsOutput:
#     """
#     List objects in an S3 bucket using Boto3 and LocalStack.
#     """
#     s3_client = get_client("s3")
#     response = s3_client.list_objects_v2(Bucket=input_data.bucket_name)
#     object_keys = [obj["Key"] for obj in response.get("Contents", [])]
#     return S3ListObjectsOutput(object_keys=object_keys)

# @store.kubiya_action()
# def get_s3_object_content(input_data: S3GetObjectInput) -> S3GetObjectOutput:
#     """
#     Get the content of an object from an S3 bucket using Boto3 and LocalStack.
#     """
#     s3_client = get_client("s3")
#     response = s3_client.get_object(Bucket=input_data.bucket_name, Key=input_data.object_key)
#     content = response["Body"].read().decode("utf-8")
#     return S3GetObjectOutput(content=content)