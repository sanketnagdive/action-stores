from typing import List

from pydantic import BaseModel


from .. import action_store
from .. bitbucket_wrapper import get_client

from ..models.repositories import (
    GetRepositoriesParams,GetRepositoriesResponse,
)



@action_store.kubiya_action()
def get_repositories(input: GetRepositoriesParams)->GetRepositoriesResponse:

    client = get_client(input.workspace)
    all_repos=client._get("2.0/repositories/{}".format(input.workspace),params=None,)


    return GetRepositoriesResponse(repos=all_repos)

# class CreatePRInput(BaseModel):
#     workspace: str
#     repository: str
#     title: str
#     source_branch: str
#     destination_branch: str
#
#
# @action_store.kubiya_action()
# def create_pull_request(input: CreatePRInput):
#     client = get_client(input.workspace)
#     res = client.create_pull_request(
#         input.repository,
#         input.title,
#         input.source_branch,
#         input.destination_branch,
#     )
#     return res
#
#
# class MergePRInput(BaseModel):
#     workspace: str
#     repository: str
#     pull_request_id: str
#
#
# @action_store.kubiya_action()
# def merge_pull_request(input: MergePRInput):
#     client = get_client(input.workspace)
#     res = client.merge_pull_request(
#         input.repository,
#         input.pull_request_id,
#     )
#     return res
#
#
# class GetOpenPullRequestsInput(BaseModel):
#     workspace: str
#     repository: str
#
#
# @action_store.kubiya_action()
# def get_open_pull_requests(input: GetOpenPullRequestsInput):
#     client = get_client(input.workspace)
#     res = list(client.all_pages(client.get_open_pull_requests, input.repository))
#     return res
