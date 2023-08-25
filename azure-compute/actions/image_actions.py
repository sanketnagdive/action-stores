import logging

from .. import action_store as action_store
from ..azure_wrapper import *
# from ..models.vmss_models import *
from ..models.image_models import *
from typing import Union

logger = logging.getLogger(__name__)

@action_store.kubiya_action()
def create_or_update_azure_image(params: ImageCreationParameters) -> Union[ImageModel, dict]:
    imageName = params.imageName
    subscriptionId = params.subscriptionId
    resourceGroupName = params.resourceGroupName
    vmName = params.vmName
    image_data = {
                "location": "West US",
                "properties": {
                "sourceVirtualMachine": {
                    "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{VMname}"
                                        }
                                }
                }
    endpoint = f"https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/images/{imageName}"
    api_version = ""
    response_data = put_wrapper(endpoint, subscriptionId, api_version, data=image_data)
    return ImageModel(**response_data)

@action_store.kubiya_action()
def get_azure_images(params: ImageCreationParameters) -> Union[ImageModel, dict]:
    subscriptionId = params.subscriptionId
    resourceGroupName = params.resourceGroupName
    imageName = params.imageName
    endpoint = f"https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/images/{imageName}"
    api_version = "2022-11-01"

    response_data = get_wrapper(endpoint, params.subscriptionId, api_version)

    return ImageModel(**response_data)

@action_store.kubiya_action()
def listall_azure_images(params: ImageListParameters) -> Union[ImageListModel, dict]:
    subscriptionId = params.subscriptionId