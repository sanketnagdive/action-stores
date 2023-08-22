from pydantic import BaseModel
from typing import Optional, List
from google.cloud import compute_v1

class CreateVmParams(BaseModel):
    project_id: str
    zone: str
    instance_name: str
    disks: list[compute_v1.AttachedDisk]
    machine_type: str = "n1-standard-1"
    network_link: str = "global/networks/default"
    subnetwork_link: str = None
    internal_ip: str = None
    external_access: bool = False
    external_ipv4: str = None
    accelerators: list[compute_v1.AcceleratorConfig] = None
    preemptible: bool = False
    spot: bool = False
    instance_termination_action: str = "STOP"
    custom_hostname: str = None
    delete_protection: bool = False