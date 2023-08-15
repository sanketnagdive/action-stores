from pydantic import BaseModel
from typing import List, Optional

class CreateSQSQueueRequest(BaseModel):
    queue_name: str

class CreateSQSQueueResponse(BaseModel):
    queue_url: str

class ListSQSQueuesRequest(BaseModel):
    pass

class ListSQSQueuesResponse(BaseModel):
    queue_urls: list

class GetSQSQueueAttributesRequest(BaseModel):
    queue_url: str

class GetSQSQueueAttributesResponse(BaseModel):
    attributes: dict

