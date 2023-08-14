from ..models.user_models import *
from ..pagerduty_wrapper import *
from .. import action_store as action_store

@action_store.kubiya_action()
def get_user(input_model: GetUserInput) -> ListUsersOutput:
    response_data = get_wrapper(f"users/{input_model.user_id}")
    return ListUsersOutput(**response_data["user"])

@action_store.kubiya_action()
def create_user(input_model: CreateUserInput) -> ListUsersOutput:
    response_data = post_wrapper("users", args=input_model.dict())
    return ListUsersOutput(**response_data["user"])
