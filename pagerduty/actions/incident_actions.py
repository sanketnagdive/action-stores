from ..models.incident_models import *
from ..pagerduty_wrapper import *
from .. import action_store as action_store

@action_store.kubiya_action()
def list_incidents(input_model: ListIncidentsInput) -> List[ListIncidentsOutput]:
    path = "incidents"
    if input_model.status:
        path += f"?status={input_model.status}"
    response_data = get_wrapper(path)
    return response_data["incidents"]

@action_store.kubiya_action()
def get_incident(input_model: GetIncidentInput) -> ListIncidentsOutput:
    response_data = get_wrapper(f"incidents/{input_model.incident_id}")
    return ListIncidentsOutput(**response_data["incident"])

@action_store.kubiya_action()
def create_incident(input_model: CreateIncidentInput) -> ListIncidentsOutput:
    # Nest the data under "incident" key
    request_data = {
        "incident": {
            "type": input_model.type,
            "title": input_model.title,
            "service": {
                "id": input_model.service_id,
                "type": "service_reference"
            },
            "urgency": input_model.urgency,
            "body": {
                "type": "incident_body",
                "details": input_model.body_details
            }
        }
    }
    
    response_data = post_wrapper("incidents", args=request_data)
    return response_data["incident"]
