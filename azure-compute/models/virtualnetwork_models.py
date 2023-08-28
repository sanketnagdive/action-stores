from pydantic import BaseModel
from typing import Optional, List

class VNETCreationParameters(BaseModel):
    vnetName: str
    subscriptionId: str
    resourceGroupName: str
    # vmName: str
    location: str
    cidr: list
    
class VirtualNetworkResponseModel(BaseModel):
    vnetName: Optional(str)
    location: Optional(str)
    properties: dict