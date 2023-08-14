from typing import List

from pydantic import BaseModel


from .. import action_store
from .. bitbucket_wrapper import get_client

from ..models.pullrequests import (
    GetOpenPullRequestsParams,GetOpenPullRequestsResponse,
    MergePrParams,MergePrResponse,
    CreatePrParams,CreatePrResponse
)


@action_store.kubiya_action()
def get_open_pull_requests(input: GetOpenPullRequestsParams)->GetOpenPullRequestsResponse:
    client = get_client(input.workspace)
    pull_requests = client._get("2.0/repositories/{}/{}/pullrequests".format(input.workspace,
                                                                             input.repository_slug),params=None,)

    return GetOpenPullRequestsResponse(pull_requests=pull_requests)




# @action_store.kubiya_action()
def merge_pull_request(input: MergePrParams):
    client = get_client(input.workspace)
    res = client._post("2.0/repositories/{}/{}/pullrequests/{}/merge".format(input.workspace,
                                                                             input.repository_slug,
                                                                             input.pull_request_id),params=None,
                                                                                                    data=None)
    return MergePrResponse(response=res)


# @action_store.kubiya_action()
def create_pull_request(input: CreatePrParams):
    client = get_client(input.workspace)
    res = client._post("2.0/repositories/{}/{}/pullrequests".format(input.workspace,input.repository_slug),
                       params=None,
                       data={"title": input.title,
                             "source": {"branch": {"name": input.source_branch}},
                             "destination": {"branch": {"name": input.destination_branch}},
                             },
                       )
    return CreatePrResponse(response=res)
