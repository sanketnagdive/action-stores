from typing import List, Any, Optional, Union
from pydantic import BaseModel
from datetime import datetime
from ..models.groups import *

from .. import action_store as action_store
from ..http_wrapper import *

@action_store.kubiya_action()
def list_groups(input: GroupList):
    response = get_wrapper(endpoint='/groups', args=input.dict(exclude_none=True))
    return Groups(groups=response)

@action_store.kubiya_action()
def list_group_subgroups(input: GroupSubgroupsList):
    response = get_wrapper(endpoint=f'/groups/{input.id}/subgroups', args=input.dict(exclude_none=True))
    return Groups(groups=response)

@action_store.kubiya_action()
def list_group_descendant_groups(input: GroupSubgroupsList):
    response = get_wrapper(endpoint=f'/groups/{input.id}/descendant_groups', args=input.dict(exclude_none=True))
    return Groups(groups=response)

@action_store.kubiya_action()
def list_group_projects(input: GroupProjectsList):
    response = get_wrapper(endpoint=f'/groups/{input.id}/projects', args=input.dict(exclude_none=True))
    return Groups(groups=response)
    
@action_store.kubiya_action()
def list_group_shared_projects(input: GroupSharedProjectsList):
    response = get_wrapper(endpoint=f'/groups/{input.id}/projects/shared', args=input.dict(exclude_none=True))
    return Group(groups=response)

@action_store.kubiya_action()
def get_group_details(input: GroupDetails):
    response = get_wrapper(endpoint=f'/groups/{input.id}')
    return Group(groups = response)

@action_store.kubiya_action()
def create_new_group(input: NewGroup):
    return post_wrapper(endpoint='/groups', args=input.dict(exclude_none=True))

@action_store.kubiya_action()
def list_group_hooks(input: ListGroupHooks):
    response = get_wrapper(endpoint=f'/groups/{input.id}/hooks', args=input.dict())
    return Hooks(hooks = response)

@action_store.kubiya_action()
def get_group_push_rules(input: GetGroupPushRules):
    response = get_wrapper(endpoint=f'/groups/{input.id}/push_rule', args=input.dict())
    return Rules(rules = response)