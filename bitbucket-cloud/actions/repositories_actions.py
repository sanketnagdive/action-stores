from typing import List

from pydantic import BaseModel


from .. import action_store
from .. bitbucket_wrapper import get_client

from ..models.repositories import (
    GetRepositoriesParams,GetRepositoriesResponse,
    GetRepositoryParams,GetRepositoryResponse,
    CreateRepositoryParams,CreateRepositoryResponse,
)

@action_store.kubiya_action()
def get_repository(input: GetRepositoryParams)->GetRepositoryResponse:

    client = get_client(input.workspace)
    repo=client._get("2.0/repositories/{}/{}".format(input.workspace,input.repo_slug),params=None)


    return GetRepositoryResponse(repo=repo)

@action_store.kubiya_action()
def create_repository(input: CreateRepositoryParams)->CreateRepositoryResponse:

    client = get_client(input.workspace)
    res= client._post("2.0/repositories/{}/{}".format(input.workspace,
                                                      input.repo_slug),
                            params=None,
                            data={"is_private": input.is_private}
                            )

    return CreateRepositoryResponse(response=res)


@action_store.kubiya_action()
def get_repositories(input: GetRepositoriesParams)->GetRepositoriesResponse:

    client = get_client(input.workspace)
    all_repos=client._get("2.0/repositories/{}".format(input.workspace),params=None)


    return GetRepositoriesResponse(repos=all_repos)