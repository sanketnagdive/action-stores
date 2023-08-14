from typing import List

from pydantic import BaseModel


from .. import action_store
from .. bitbucket_wrapper import get_client

from ..models.issues import (
    GetIssueParams,GetIssueResponse,
    GetIssuesParams,GetIssuesResponse,
    CreateIssueParams,CreateIssueResponse,
    DeleteIssueParams,DeleteIssueResponse,
)


# @action_store.kubiya_action()
def get_issue(input: GetIssueParams )->GetIssueResponse:
    client = get_client(input.workspace)
    issue = client._get("2.0/repositories/{}/{}/issues/{}".format(input.workspace,
                                                                          input.repository_slug,
                                                                          input.issue_id),params=None,)

    return GetIssueResponse(issue=issue)


@action_store.kubiya_action()
def get_issues(input: GetIssuesParams )->GetIssuesResponse:
    client = get_client(input.workspace)
    issues = client._get("2.0/repositories/{}/{}/issues".format(input.workspace,
                                                                input.repository_slug),params=None,)

    return GetIssuesResponse(issues=issues)
@action_store.kubiya_action()
def create_issue(input: CreateIssueParams )->CreateIssueResponse:
    client=get_client(input.workspace)
    issue = client._post("2.0/repositories/{}/{}/issues".format(input.workspace,input.repo_slug),
                         data={"type":input.type,
                               "title": input.title,
                               "kind": input.type,
                                 "priority": input.priority,
                               "content": {"raw": input.content}},
                         params=None)

    return CreateIssueResponse(issue=issue)

# @action_store.kubiya_action()
def delete_issue(input: DeleteIssueParams )->DeleteIssueResponse:
    client=get_client(input.workspace)
    response = client._delete("2.0/repositories/{}/{}/issues/{}".format(input.workspace,
                                                                     input.repo_slug,
                                                                     input.issue_id),params=None,)

    # # Check if the response status code is 204 (the base client returns empty string for 204 responses)
    if response == '':
        # If it's a 204 response, return an empty dictionary
        return DeleteIssueResponse(issue={})

    # If it's not a 204 response, assume it has a JSON response
    issue_data = response.json()
    return DeleteIssueResponse(issue=issue_data)