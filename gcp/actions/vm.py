from .. import action_store as action_store
from models.vm import *
from ..gcp_wrapper import clients_networks

import re
import sys
from typing import Any
import warnings

from google.cloud import compute_v1

@action_store.kubiya_action()    
def create_instance(params: CreateVmParams):    
    instance_client = compute_v1.InstancesClient()

    # Use the network interface provided in the network_link argument.
    network_interface = compute_v1.NetworkInterface()
    network_interface.network = params.network_link
    if params.subnetwork_link:
        network_interface.subnetwork = params.subnetwork_link

    if params.internal_ip:
        network_interface.network_i_p = params.internal_ip

    if params.external_access:
        access = compute_v1.AccessConfig()
        access.type_ = compute_v1.AccessConfig.Type.ONE_TO_ONE_NAT.name
        access.name = "External NAT"
        access.network_tier = access.NetworkTier.PREMIUM.name
        if params.external_ipv4:
            access.nat_i_p = params.external_ipv4
        network_interface.access_configs = [access]

    # Collect information into the Instance object.
    instance = compute_v1.Instance()
    instance.network_interfaces = [network_interface]
    instance.name = params.instance_name
    instance.disks = params.disks
    if re.match(r"^zones/[a-z\d\-]+/machineTypes/[a-z\d\-]+$", params.machine_type):
        instance.machine_type = params.machine_type
    else:
        instance.machine_type = f"zones/{params.zone}/machineTypes/{params.machine_type}"

    instance.scheduling = compute_v1.Scheduling()
    if params.accelerators:
        instance.guest_accelerators = params.accelerators
        instance.scheduling.on_host_maintenance = (
            compute_v1.Scheduling.OnHostMaintenance.TERMINATE.name
        )

    if params.preemptible:
        # Set the preemptible setting
        warnings.warn(
            "Preemptible VMs are being replaced by Spot VMs.", DeprecationWarning
        )
        instance.scheduling = compute_v1.Scheduling()
        instance.scheduling.preemptible = True

    if params.spot:
        # Set the Spot VM setting
        instance.scheduling.provisioning_model = (
            compute_v1.Scheduling.ProvisioningModel.SPOT.name
        )
        instance.scheduling.instance_termination_action = params.instance_termination_action

    if params.custom_hostname is not None:
        # Set the custom hostname for the instance
        instance.hostname = params.custom_hostname

    if params.delete_protection:
        # Set the delete protection bit
        instance.deletion_protection = True

    # Prepare the request to insert an instance.
    request = compute_v1.InsertInstanceRequest()
    request.zone = params.zone
    request.project = params.project_id
    request.instance_resource = instance

    # Wait for the create operation to complete.
    print(f"Creating the {params.instance_name} instance in {params.zone}...")

    operation = instance_client.insert(request=request)

    params.wait_for_extended_operation(operation, "instance creation")

    print(f"Instance {params.instance_name} created.")
    return instance_client.get(project=params.project_id, zone=params.zone, instance=params.instance_name)
