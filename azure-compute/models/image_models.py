from pydantic import BaseModel
from typing import Optional, List

class ImageCreationParameters(BaseModel):
    imageName: str
    subscriptionId: str
    resourceGroupName: str
    vmName: str
    location: str
    
class ImageModel(BaseModel):
    id: str
    type: str
    name: str
    location: str
    tags: Optional[dict] = {}
    properties: dict
    
class ImageListParameters(BaseModel):
    subscribtionId: str
    
class ImageListModel(BaseModel):
    imageName: str
    location: str
    id: str
    properties: dict
    tags: Optional[dict] = {}
    