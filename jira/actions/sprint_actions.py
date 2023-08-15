from ..jira_wrapper import get_jira_instance
from ..models.sprint import SprintParams, SprintResponse, AddIssueToSprintParams, AddIssueToSprintResponse, GetAllSprintsParams, GetAllSprintsResponse
from .. import action_store as action_store


@action_store.kubiya_action()
def start_sprint(request: SprintParams) -> SprintResponse:
    """
    Creates a new sprint and returns the sprint data
    """
    jira = get_jira_instance()
    sprint = jira.create_sprint(request.dict())
    return SprintResponse(**sprint)

@action_store.kubiya_action()
def add_issue_to_sprint(request: AddIssueToSprintParams) -> AddIssueToSprintResponse:
    """
    Adds an issue to a sprint and returns the sprint data
    """
    jira = get_jira_instance()
    success = jira.add_issues_to_sprint(request.sprint_id, [request.issue_key])
    return AddIssueToSprintResponse(success=success)

@action_store.kubiya_action()
def get_all_sprints(request: GetAllSprintsParams) -> GetAllSprintsResponse:
    """
    Gets all sprints for a board and returns the sprint data
    """
    jira = get_jira_instance()
    sprints = jira.sprints(board_id=2)
    return GetAllSprintsResponse(sprints=sprints)