import logging

from .. import action_store as action_store
from ..azure_wrapper import *
from ..models.vm_models import *
from typing import Union

logger = logging.getLogger(__name__)


@action_store.kubiya_action()
def create_or_update_virtual_machine(params: VMCreationParameters) -> Union[VirtualMachineResponseModel, dict]:
    subscriptionId = params.subscriptionId
    resourceGroupName = params.resourceGroupName
    vmName = params.vmName
    networkInterfaceName = params.networkInterfaceName
    vm_data = {
        "location": params.location,
        "properties": {
            "hardwareProfile": {"vmSize": params.vmSize},
            "osProfile": {
                "computerName": params.computer_name,
                "adminUsername": params.admin_username,
                "adminPassword": params.admin_password,
            },
            "storageProfile": {
                "imageReference": {
                    "publisher": params.publisher,
                    "offer": params.offer,
                    "sku": params.sku,
                    "version": params.version,
                },
            },
            "networkProfile": {
                "networkInterfaces": [
                    {
                        "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/networkInterfaces/{networkInterfaceName}",
                        "properties": {
                            "primary": True
                        }
                    }
                ]
            }
        }
    }

    endpoint = f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{vmName}"
    api_version = "2023-03-01"

    response_data = put_wrapper(endpoint, subscriptionId, api_version, data=vm_data)

    return VirtualMachineResponseModel(**response_data)



@action_store.kubiya_action()
def get_virtual_machine(params: VMQueryParameters) -> Union[VirtualMachineResponseModel, dict]:
    subscriptionId = params.subscriptionId
    resourceGroupName = params.resourceGroupName
    vmName = params.vmName

    endpoint = f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{vmName}"
    api_version = "2023-03-01"

    response_data = get_wrapper(endpoint, subscriptionId, api_version)

    return VirtualMachineResponseModel(**response_data)



@action_store.kubiya_action()
def list_all_virtual_machines(params: VMListParameters) -> List[VirtualMachineListModel]:
    endpoint = f"/subscriptions/{params.subscriptionId}/providers/Microsoft.Compute/virtualMachines"
    api_version = "2023-03-01"

    response_data = get_wrapper(endpoint, params.subscriptionId, api_version)

    vm_list = response_data.get('value', [])
    return [VirtualMachineListModel(**vm) for vm in vm_list]



@action_store.kubiya_action()
def get_subscriptions(params: SubscriptionQueryParameters) -> Union[SubscriptionListResult, dict]:
    endpoint = "/subscriptions"
    api_version = "2020-01-01"

    response_data = get_wrapper(endpoint, '', api_version)

    return SubscriptionListResult(**response_data)



@action_store.kubiya_action()
def get_resource_groups(params: RGQueryParameters) -> Union[ResourceGroupListResult, dict]:
    subscriptionId = params.subscriptionId
    endpoint = f"/subscriptions/{subscriptionId}/resourcegroups"
    api_version = "2021-04-01"

    response_data = get_wrapper(endpoint, subscriptionId, api_version)

    if response_data:
        return ResourceGroupListResult(**response_data)
    else:
        return None
    


@action_store.kubiya_action()
def get_network_interfaces(params: NetworkInterfaceParams) -> Union[NetworkInterfaceListResult, dict]:
    endpoint = f"/subscriptions/{params.subscriptionId}/resourceGroups/{params.resourceGroupName}/providers/Microsoft.Network/networkInterfaces"
    api_version = "2022-11-01"

    response_data = get_wrapper(endpoint, params.subscriptionId, api_version)

    return NetworkInterfaceListResult(**response_data)



@action_store.kubiya_action()
def get_publishers(params: PublisherParams):
    endpoint = f"/subscriptions/{params.subscriptionId}/providers/Microsoft.Compute/locations/{params.location}/publishers"
    api_version = "2023-03-01"

    response_data = get_wrapper(endpoint, "", api_version)

    return response_data



@action_store.kubiya_action()
def get_locations(params: LocationParams): 
    endpoint = f"/subscriptions/{params.subscriptionId}/locations"
    api_version = "2020-01-01"

    response_data = get_wrapper(endpoint, "", api_version)

    return response_data



@action_store.kubiya_action()
def get_versions(params: VersionsParams):
    endpoint = f"/subscriptions/{params.subscriptionId}/providers/Microsoft.Compute/locations/{params.location}/publishers/{params.publisherName}/artifacttypes/vmimage/offers/{params.offer}/skus/{params.skus}/versions"
    api_version = "2023-03-01"

    response_data = get_wrapper(endpoint, "", api_version)

    return response_data



@action_store.kubiya_action()
def get_skus(params: SkusParams):
    endpoint = f"/subscriptions/{params.subscriptionId}/providers/Microsoft.Compute/locations/{params.location}/publishers/{params.publisherName}/artifacttypes/vmimage/offers/{params.offer}/skus"
    api_version = "2023-03-01"

    response_data = get_wrapper(endpoint, "", api_version)

    return response_data



@action_store.kubiya_action()
def get_machine_sizes(params: MachineSizesParams):
    endpoint = f"/subscriptions/{params.subscriptionId}/providers/Microsoft.Compute/locations/{params.location}/vmSizes"
    api_version = "2023-03-01"

    response_data = get_wrapper(endpoint, "", api_version)

    return response_data

