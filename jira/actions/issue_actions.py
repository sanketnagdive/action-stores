from ..jira_wrapper import get_jira_instance
from atlassian import Jira
from ..models.issue import CreateIssueParams, CreateIssueResponse, \
    UpdateIssueParams, AssignIssueParams, \
    UpdateIssueResponse, \
    GetAllIssuesParams, GetAllIssuesResponse, \
    TransitionIssueParams, TransitionIssueResponse
from ..models.common import SimpleResponse
from .. import action_store as action_store

def get_jira_url(issue_key: str, jira_instance: Jira) -> str:
    """
    Returns the URL of an issue
    """
    return jira_instance.url + '/browse/' + issue_key

@action_store.kubiya_action()
def create_issue(request: CreateIssueParams) -> CreateIssueResponse:
    """
    Creates a Jira ticket and returns the issue key and URL
    """
    jira = get_jira_instance()
    issue = jira.issue_create(
        fields={
            "project": {"key": "KUB"},
            "issuetype": {"name": request.issue_type_name},
            "summary": request.summary,
            "description": request.description,
        }
    )
    issue_url = get_jira_url(issue['key'], jira)
    return CreateIssueResponse(issue_url=issue_url, **issue)

@action_store.kubiya_action()
def transition_issue(request: TransitionIssueParams) -> TransitionIssueResponse:
    """
    Transitions a Jira ticket and returns the issue key and URL
    """
    jira = get_jira_instance()
    success = jira.issue_transition(issue_key=request.issue_key, status=request.transition_name)
    return TransitionIssueResponse(success=success)

@action_store.kubiya_action()
def update_issue(request: UpdateIssueParams) -> UpdateIssueResponse:
    """
    Updates a Jira ticket and returns the issue key and URL
    """
    jira = get_jira_instance()

    update_dict = {}
    updated_fields = []

    if request.summary:
        update_dict['summary'] = request.summary
        updated_fields.append('summary')
    if request.description:
        update_dict['description'] = request.description
        updated_fields.append('description')

    if update_dict:
        jira.update_issue_field(request.issue_key, update_dict)
        
        # Construct the response message based on the updated fields
        if updated_fields:
            success = True
            message = f"Updated fields {', '.join(updated_fields)} for issue {request.issue_key}."
        else:
            success = False
            message = f"No fields to update for issue {request.issue_key}."
    else:
        success = False
        message = f"No fields to update for issue {request.issue_key}."

    response = UpdateIssueResponse(success=success, message=message)
    return response

@action_store.kubiya_action()
def assign_issue(request: AssignIssueParams) -> SimpleResponse:
    """
    Assigns a Jira ticket to a user and returns the issue key and URL
    """
    jira = get_jira_instance()
    issue = jira.assign_issue(request.issue_key, "63d701e4790148a18092b345")
    return SimpleResponse(message=f"Issue {request.issue_key} assigned to {request.assignee_name} successfully.")

@action_store.kubiya_action()
def get_all_issues(request: GetAllIssuesParams) -> GetAllIssuesResponse:
    """
    Gets all issues in a project and returns the issue key and URL
    """
    jira = get_jira_instance()
    issues = jira.search_issues('project=KUB')
    return GetAllIssuesResponse(issues=issues)