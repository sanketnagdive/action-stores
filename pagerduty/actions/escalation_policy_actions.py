from ..models.escalation_policy_models import *
from ..pagerduty_wrapper import *
from typing import List
from .. import action_store as action_store

@action_store.kubiya_action()
def list_policies(input_model: ListPoliciesInput) -> List[ListPoliciesOutput]:
    response_data = get_wrapper("escalation_policies")
    return [ListPoliciesOutput(**policy) for policy in response_data["escalation_policies"]]

@action_store.kubiya_action()
def get_policy(input_model: GetPolicyInput) -> ListPoliciesOutput:
    response_data = get_wrapper(f"escalation_policies/{input_model.policy_id}")
    return ListPoliciesOutput(**response_data["escalation_policy"])
