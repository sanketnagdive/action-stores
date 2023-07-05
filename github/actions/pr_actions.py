from github import GithubException, PullRequest
from ..github_wrapper import get_github_instance, get_entity
from ..models.pull_request import (
    ListOpenPRsParams, ListOpenPRsResponse,
    GetPRDetailsParams, GetPRDetailsResponse, GetRepoPullRequestsParams, GetRepoPullRequestsResponse
)
from .. import action_store as action_store
import logging

logger = logging.getLogger(__name__)

@action_store.kubiya_action()
def list_open_prs(params: ListOpenPRsParams) -> ListOpenPRsResponse:
    try:
        github = get_github_instance()
        entity = get_entity(github)
        repo = entity.get_repo(params.repo_name)
        prs = [pr.html_url for pr in repo.get_pulls(state="open")]
        return ListOpenPRsResponse(prs=prs)
    except GithubException as e:
        logger.error(f"Failed to list open pull requests: {e}")
        raise

@action_store.kubiya_action()
def get_pr_details(params: GetPRDetailsParams) -> GetPRDetailsResponse:
    try:
        github = get_github_instance()
        entity = get_entity(github)
        repo = entity.get_repo(params.repo_name)
        pr = repo.get_pull(params.pr_number)
        return GetPRDetailsResponse(pr_url=pr.html_url, title=pr.title, body=pr.body, state=pr.state)
    except GithubException as e:
        logger.error(f"Failed to get pull request details: {e}")
        raise
@action_store.kubiya_action()
def get_repo_pull_requests(params: GetRepoPullRequestsParams) -> GetRepoPullRequestsResponse:
    try:
        github = get_github_instance()
        entity = get_entity(github)
        repo = entity.get_repo(params.repo_name)
        prs = [pr for pr in repo.get_pulls(state=params.state)]
        return GetRepoPullRequestsResponse(prs=prs)
    except GithubException as e:
        logger.error(f"Failed to get pull requests: {e}")
        raise