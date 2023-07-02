from ..jira_wrapper import get_jira_instance
from ..models.sprint import SprintParams, SprintResponse, EndSprintParams, EndSprintResponse, AddIssueToSprintParams, AddIssueToSprintResponse, GetAllSprintsParams, GetAllSprintsResponse
from .. import action_store as action_store


@action_store.kubiya_action()
def start_sprint(request: SprintParams) -> SprintResponse:
    jira = get_jira_instance()
    sprint = jira.sprint_create(request.dict())
    return SprintResponse(**sprint)

@action_store.kubiya_action()
def end_sprint(request: EndSprintParams) -> EndSprintResponse:
    jira = get_jira_instance()
    success = jira.sprint_end(request.sprint_id)
    return EndSprintResponse(success=success)

@action_store.kubiya_action()
def add_issue_to_sprint(request: AddIssueToSprintParams) -> AddIssueToSprintResponse:
    jira = get_jira_instance()
    success = jira.add_issues_to_sprint(request.sprint_id, [request.issue_key])
    return AddIssueToSprintResponse(success=success)

@action_store.kubiya_action()
def get_all_sprints(request: GetAllSprintsParams) -> GetAllSprintsResponse:
    jira = get_jira_instance()
    sprints = jira.sprints(board_id=request.board_id)
    return GetAllSprintsResponse(sprints=sprints)