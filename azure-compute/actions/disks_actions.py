import logging

from .. import action_store as action_store
from ..azure_wrapper import *
from ..models.vm_models import *
from typing import Union

logger = logging.getLogger(__name__)


@action_store.kubiya_action()
def create_or_update_disks(params: DiskCreationParameters) -> Union[DiskResponseModel, dict]:
    subscriptionId = params.subscriptionId
    resourceGroupName = params.resourceGroupName
    diskName = params.diskName
    disk_data = {
                "location": params.location,
                "properties": {
                    "creationData": {
                    "createOption": "Empty"
                    },
                    "diskSizeGB": params.diskSizeGB
                }
                }
    endpoint = f"subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/disks/{diskName}"
    api_version = "2023-03-01"

    response_data = put_wrapper(endpoint, subscriptionId, api_version, data=vnet_data)

    return DiskResponseModel(**response_data)

@action_store.kubiya_action()
def get_disks(params: DiskCreationParameters) -> Union[DiskResponseModel, dict]:
    subscriptionId = params.subscriptionId
    resourceGroupName = params.resourceGroupName
    vnetName = params.vnetName
    api_version = ""
    endpoint = f"subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/disks/{diskName}"
    response_data = get_wrapper(endpoint, subscriptionId, api_version)
    return DiskResponseModel(**response_data)

@action_store.kubiya_action()
def listall_azure_disks(params: DiskListParameters) -> Union[DiskListModel, dict]:
    #subscriptionId = params.subscriptionId
    endpoint = f"subscriptions/{params.subscriptionId}/providers/Microsoft.Compute/disks"
    api_version = "2022-11-01"
    response_data = get_wrapper(endpoint, params.subscriptionId, api_version)
    disk_list = response_data.get('value', [])
    return [DiskListModel(**disk) for disk in disk_list]

def list_by_rg_azure_disks(params: DiskListParameters) -> Union[DiskListModel, dict]:
    #subscriptionId = params.subscriptionId
    endpoint = f"subscriptions/{params.subscriptionId}/resourceGroups/{params.resourceGroupName}/providers/Microsoft.Compute/disks"
    api_version = "2022-11-01"
    response_data = get_wrapper(endpoint, params.subscriptionId, api_version)
    disk_list = response_data.get('value', [])
    return [DiskListModel(**disk) for disk in disk_list]