from typing import List

from pydantic import BaseModel


from .. import action_store
from .. bitbucket_wrapper import get_client

from ..models.sources import (
    GetFileContentParams, GetFileContentResponse
)


@action_store.kubiya_action()
def get_file_content(input: GetFileContentParams)->GetFileContentResponse:
    client = get_client(input.workspace)

    file_content=client._get("2.0/repositories/{}/{}/src/{}/{}".format(input.workspace,
                                                                       input.repository,
                                                                       input.commit_id,
                                                                       input.file_path),params=None)

    return GetFileContentResponse(content=file_content)