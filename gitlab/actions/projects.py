from typing import List, Any, Optional, Union, Dict
from pydantic import BaseModel, Field, parse_obj_as
from datetime import datetime
from ..models.projects import *

from .. import action_store as action_store
from ..http_wrapper import *

@action_store.kubiya_action()
def list_all_projects(input: ProjectListRequest):
    response = get_wrapper(endpoint=f'/projects', args=input.dict(exclude_none=True))
    return Projects(projects=response)

@action_store.kubiya_action()
def list_user_projects(input: UsersUseridProjects):
    response = get_wrapper(endpoint=f'/users/{input.user_id}/projects', args=input.dict(exclude_none=True))
    return Projects(projects=response)

@action_store.kubiya_action()
def list_projects_a_user_has_contributed_to(input: ListContributed):
    response = get_wrapper(endpoint = f'/users/{input.user_id}/contributed_projects', args = input.dict(exclude_none = True))
    return Projects(projects=response)

@action_store.kubiya_action()
def list_projects_starred_by_a_user(input: UsersUseridProjects):
    response = get_wrapper(endpoint=f'/users/{input.user_id}/starred_projects', args=input.dict(exclude_none=True))
    return Projects(projects=response)

@action_store.kubiya_action()
def get_single_project(input: ProjectsIdSingleProjectSingle):
    response = get_wrapper(endpoint=f'/projects/{input.id}', args=input.dict(exclude_none=True))
    return SingleProject(projects=response)

@action_store.kubiya_action()
def get_project_users(input: ProjectsIdUsers):
    response = get_wrapper(endpoint=f'/projects/{input.id}/users', args=input.dict(exclude_none=True))
    return Users(users = response)

@action_store.kubiya_action()
def list_a_projects_groups(input: ProjectsIdGroups):
    response = get_wrapper(endpoint=f'/projects/{input.id}/groups', args=input.dict(exclude_none=True))
    return Groups(groups = response)

@action_store.kubiya_action()
def list_a_projects_shareable_groups(input: ProjectsIdSharelocations):
    response = get_wrapper(endpoint=f'/projects/{input.id}/share_locations', args=input.dict(exclude_none=True))
    return Groups(groups = response)

@action_store.kubiya_action()
def create_project(input: CreateProjectRequest):
    response = post_wrapper(endpoint='/projects', args=input.dict(exclude_none=True))
    return SingleProject(projects=response)

@action_store.kubiya_action()
def edit_project(input: ProjectsIdEdit):
    response = put_wrapper(endpoint=f'/projects/{input.id}', args=input.dict(exclude_none=True))
    return SingleProject(projects=response)