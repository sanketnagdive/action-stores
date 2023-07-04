from ..jira_wrapper import get_jira_instance
from atlassian import Jira
from ..models.issue import CreateIssueParams, CreateIssueResponse, \
    CommentIssueParams, CommentIssueResponse, \
    UpdateIssueParams, AssignIssueParams, \
    UpdateIssueResponse, DeleteIssueParams, DeleteIssueResponse, \
    GetAllIssuesParams, GetAllIssuesResponse, \
    LinkIssuesParams, LinkIssuesResponse, \
    TransitionIssueParams, TransitionIssueResponse
from ..models.jql import RunJQLParams, RunJQLResponse
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
    Creates an issue and returns the issue key and URL
    """
    jira = get_jira_instance()
    issue = jira.issue_create(
        fields={
            "project": {"key": request.project_key},
            "issuetype": {"name": request.issue_type_name},
            "summary": request.summary,
            "description": request.description,
        }
    )
    issue_url = get_jira_url(issue['key'], jira)
    return CreateIssueResponse(issue_url=issue_url, **issue)
@action_store.kubiya_action()
def create_issue(request: CreateIssueParams) -> CreateIssueResponse:
    """
    Creates an issue and returns the issue key and URL
    """
    jira = get_jira_instance()
    issue = jira.issue_create(
        fields={
            "project": {"key": request.project_key},
            "issuetype": {"name": request.issue_type_name},
            "summary": request.summary,
            "description": request.description,
        }
    )
    return CreateIssueResponse(**issue)

@action_store.kubiya_action()
def transition_issue(request: TransitionIssueParams) -> TransitionIssueResponse:
    """
    Transitions an issue and returns the issue key and URL
    """
    jira = get_jira_instance()
    success = jira.transition_issue(issue_key=request.issue_key, transition=request.transition_name)
    return TransitionIssueResponse(success=success)

@action_store.kubiya_action()
def link_issues(request: LinkIssuesParams) -> LinkIssuesResponse:
    """
    Links two issues and returns the issue key and URL
    """
    jira = get_jira_instance()
    success = jira.link_issues(issue1=request.issue_key_1, issue2=request.issue_key_2, type=request.link_type_name)
    return LinkIssuesResponse(success=success)

@action_store.kubiya_action()
def comment_issue(request: CommentIssueParams) -> CommentIssueResponse:
    """
    Comments on an issue and returns the comment ID
    """
    jira = get_jira_instance()
    comment = jira.add_comment(request.issue_key, request.body)
    return CommentIssueResponse(**comment)

@action_store.kubiya_action()
def update_issue(request: UpdateIssueParams) -> UpdateIssueResponse:
    """
    Updates an issue and returns the issue key and URL
    """
    jira = get_jira_instance()
    success = jira.update_issue(request.issue_key, request.update_dict)
    return UpdateIssueResponse(success=success)

@action_store.kubiya_action()
def assign_issue(request: AssignIssueParams) -> SimpleResponse:
    """
    Assigns an issue to a user and returns the issue key and URL
    """
    jira = get_jira_instance()
    issue = jira.assign_issue(request.issue_key, request.assignee_name)
    return SimpleResponse(message=f"Issue {request.issue_key} assigned to {request.assignee_name} successfully.")

@action_store.kubiya_action()
def delete_issue(request: DeleteIssueParams) -> DeleteIssueResponse:
    """
    Deletes an issue and returns the issue key and URL
    """
    jira = get_jira_instance()
    success = jira.delete_issue(request.issue_key)
    return DeleteIssueResponse(success=success)

@action_store.kubiya_action()
def get_all_issues(request: GetAllIssuesParams) -> GetAllIssuesResponse:
    """
    Gets all issues in a project and returns the issue key and URL
    """
    jira = get_jira_instance()
    issues = jira.search_issues('project={}'.format(request.project_key))
    return GetAllIssuesResponse(issues=issues)