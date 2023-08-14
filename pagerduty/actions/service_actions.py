from ..models.service_models import *
from ..pagerduty_wrapper import *
from typing import List
from .. import action_store as action_store

@action_store.kubiya_action()
def list_services(input_model: ListServicesInput) -> List[ListServicesOutput]:
    response_data = get_wrapper("services")
    return [ListServicesOutput(**service) for service in response_data["services"]]

@action_store.kubiya_action()
def get_service(input_model: GetServiceInput) -> ListServicesOutput:
    response_data = get_wrapper(f"services/{input_model.service_id}")
    return ListServicesOutput(**response_data["service"])
