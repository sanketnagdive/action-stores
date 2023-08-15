from pydantic import BaseModel
from typing import List

class CreateS3BucketRequest(BaseModel):
    bucket_name: str

class ListS3BucketsRequest(BaseModel):
    pass