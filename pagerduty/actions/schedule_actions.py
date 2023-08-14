from ..models.schedule_models import *
from ..pagerduty_wrapper import *
from typing import List
from .. import action_store as action_store


@action_store.kubiya_action()
def list_schedules(input_model: ListSchedulesInput) -> List[ListSchedulesOutput]:
    response_data = get_wrapper("schedules")
    return [ListSchedulesOutput(**schedule) for schedule in response_data["schedules"]]

@action_store.kubiya_action()
def get_schedule(input_model: GetScheduleInput) -> ListSchedulesOutput:
    response_data = get_wrapper(f"schedules/{input_model.schedule_id}")
    return ListSchedulesOutput(**response_data["schedule"])
