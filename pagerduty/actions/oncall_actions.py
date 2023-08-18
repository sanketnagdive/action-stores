from ..models.oncall_models import *
from ..pagerduty_wrapper import *
from .. import action_store as action_store

@action_store.kubiya_action()
def get_current_oncall(input_model: CurrentOnCallInput) -> CurrentOnCallOutput:
    response_data = get_wrapper(f"oncalls")
    return response_data["oncalls"]
