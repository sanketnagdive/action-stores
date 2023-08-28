import logging

from .. import action_store as action_store
from ..azure_wrapper import *
# from ..models.vms_models import *
from ..models.snapshot_models import *
from typing import Union

logger = logging.getLogger(__name__)

# @action_store.kubiya_action()
# def create_or_update_azure_snapshots(params: snapshotsCreationParameters) -> Union[snapshotsModel, dict]:
#     snapshotsName = params.snapshotsName
#     subscriptionId = params.subscriptionId
#     resourceGroupName = params.resourceGroupName
#     vmName = params.vmName
#     snapshots_data = {
#                 "location": "West US",
#                 "properties": {
#                 "sourceVirtualMachine": {
#                     "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{VMname}"
#                                         }
#                                 }
#                 }
#     endpoint = f"subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/snapshots/{snapshotsName}"
#     api_version = ""
#     response_data = put_wrapper(endpoint, subscriptionId, api_version, data=snapshots_data)
#     return snapshotsModel(**response_data)

@action_store.kubiya_action()
def get_azure_snapshots(params: snapshotsCreationParameters) -> Union[snapshotsModel, dict]:
    subscriptionId = params.subscriptionId
    resourceGroupName = params.resourceGroupName
    snapshotsName = params.snapshotsName
    endpoint = f"subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/snapshots/{snapshotsName}"
    api_version = "2021-12-01"

    response_data = get_wrapper(endpoint, params.subscriptionId, api_version)

    return snapshotsModel(**response_data)

@action_store.kubiya_action()
def listall_azure_snapshots(params: snapshotsListParameters) -> Union[snapshotsListModel, dict]:
    #subscriptionId = params.subscriptionId
    endpoint = f"subscriptions/{params.subscriptionId}/providers/Microsoft.Compute/snapshots"
    api_version = "2022-11-01"
    response_data = get_wrapper(endpoint, params.subscriptionId, api_version)
    snapshots_list = response_data.get('value', [])
    return [snapshotsListModel(**snapshots) for snapshots in snapshots_list]

def list_by_rg_azure_snapshots(params: snapshotsListParameters) -> Union[snapshotsListModel, dict]:
    #subscriptionId = params.subscriptionId
    endpoint = f"subscriptions/{params.subscriptionId}/resourceGroups/{params.resourceGroupName}/providers/Microsoft.Compute/snapshots"
    api_version = "2022-11-01"
    response_data = get_wrapper(endpoint, params.subscriptionId, api_version)
    snapshots_list = response_data.get('value', [])
    return [snapshotsListModel(**snapshots) for snapshots in snapshots_list]
    