from pydantic import BaseModel
from typing import Optional, List


class VMCreationParameters(BaseModel):
    subscriptionId: str
    resourceGroupName: str
    vmName: str
    networkInterfaceName: str
    location: str
    vmSize: str
    computer_name: str
    admin_username: str
    admin_password: str
    publisher: str
    offer: str
    sku: str
    version: str


class VirtualMachineResponseModel(BaseModel):
    name: Optional[str]
    id: Optional[str]
    type: Optional[str]
    location: Optional[str]
    tags: Optional[dict]
    properties: dict


class VMQueryParameters(BaseModel):
    subscriptionId: str
    resourceGroupName: str
    vmName: str


class VirtualMachineListModel(BaseModel):
    id: str
    name: str
    type: str
    location: str
    properties: dict
    tags: Optional[dict] = {}


class VMListParameters(BaseModel):
    subscriptionId: str


class ManagedByTenant(BaseModel):
    tenantId: str


class SubscriptionPolicies(BaseModel):
    locationPlacementId: str
    quotaId: str
    spendingLimit: str


class Subscription(BaseModel):
    id: str
    subscriptionId: str
    tenantId: str
    displayName: str
    state: str
    subscriptionPolicies: SubscriptionPolicies
    authorizationSource: str
    managedByTenants: List[ManagedByTenant]
    tags: Optional[dict] = {}
    tenantId: str


class SubscriptionListResult(BaseModel):
    value: List[Subscription]
    nextLink: Optional[str]


class SubscriptionQueryParameters(BaseModel):
    pass


class ResourceGroupProperties(BaseModel):
    provisioningState: str


class ResourceGroup(BaseModel):
    id: str
    location: str
    managedBy: Optional[str] = None
    name: str
    properties: ResourceGroupProperties
    tags: Optional[dict] = {}
    type: str


class ResourceGroupListResult(BaseModel):
    nextLink: Optional[str] = None
    value: List[ResourceGroup]


class RGQueryParameters(BaseModel):
    subscriptionId: str


class PublicIPAddress(BaseModel):
    id: str


class Subnet(BaseModel):
    id: str


class IPConfigurationProperties(BaseModel):
    provisioningState: str
    privateIPAddress: str
    privateIPAllocationMethod: str
    publicIPAddress: Optional[PublicIPAddress]
    subnet: Subnet
    primary: bool
    privateIPAddressVersion: str


class IPConfiguration(BaseModel):
    name: str
    id: str
    properties: IPConfigurationProperties


class NetworkInterfaceProperties(BaseModel):
    provisioningState: str
    ipConfigurations: List[IPConfiguration]
    dnsSettings: dict
    enableAcceleratedNetworking: bool
    enableIPForwarding: bool


class NetworkInterface(BaseModel):
    name: str
    id: str
    location: str
    properties: NetworkInterfaceProperties
    type: str


class NetworkInterfaceListResult(BaseModel):
    value: List[NetworkInterface]


class NetworkInterfaceParams(BaseModel):
    subscriptionId: str
    resourceGroupName: str


class PublisherParams(BaseModel):
    subscriptionId: str
    location: str


class LocationParams(BaseModel):
    subscriptionId: str


class OfferParams(BaseModel):
    subscriptionId: str
    location: str
    publisherName: str


class VersionsParams(BaseModel):
    subscriptionId: str
    location: str
    publisherName: str
    offer: str
    skus: str


class SkusParams(BaseModel):
    subscriptionId: str
    location: str
    publisherName: str
    offer: str


class MachineSizesParams(BaseModel):
    subscriptionId: str
    location: str