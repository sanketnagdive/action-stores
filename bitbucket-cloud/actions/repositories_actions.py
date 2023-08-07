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
    all_repos=client._get("2.0/repositories/{}".format(input.workspace),params=None)


    return GetRepositoriesResponse(repos=all_repos)
