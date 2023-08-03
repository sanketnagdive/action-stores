from typing import List

from pydantic import BaseModel


from .. import action_store
from .. bitbucket_wrapper import get_client

from ..models.refs import (
    GetRepositoryBranchesParams, GetRepositoryBranchesResponse
)


@action_store.kubiya_action()
def get_repository_branches(input: GetRepositoryBranchesParams)->GetRepositoryBranchesResponse:
    client = get_client(input.workspace)
    all_branches = client._get("2.0/repositories/{}/{}/refs/branches".format(input.workspace,
                                                                             input.repository_slug),params=None,)

    return GetRepositoryBranchesResponse(branches=all_branches)
