from typing import List

from pydantic import BaseModel


from .. import action_store
from .. bitbucket_wrapper import get_client

from ..models.sources import (
    GetFileContentParams, GetFileContentResponse,
    UploadFileParams, UploadFileResponse,
    GetRepositoryStructureParams, GetRepositoryStructureResponse,
)


@action_store.kubiya_action()
def get_file_content(input: GetFileContentParams)->GetFileContentResponse:
    client = get_client(input.workspace)
    file_content=client._get("2.0/repositories/{}/{}/src/{}/{}".format(input.workspace,
                                                                       input.repository,
                                                                       input.commit_id,
                                                                       input.file_path),params=None)

    return GetFileContentResponse(content=file_content)


@action_store.kubiya_action()
def upload_file(input: UploadFileParams)->UploadFileResponse:
    client = get_client(input.workspace)

    """files ex.
        files = {
            "folder123/file1": ("file1", "content"),
            "folder123/file2": ("file2", "content2"),
        }
        """

    res= client._post_files("2.0/repositories/{}/{}/src".format(input.workspace,
                                                                input.repository_slug),
                            params=None,
                            data={"message": input.commit_message,"branch": input.branch,},
                            files={input.file_path: input.file_content},
    )

    return res


@action_store.kubiya_action()
def get_repository_structure(input: GetRepositoryStructureParams)->GetRepositoryStructureResponse:
    client = get_client(input.workspace)
    resp=client._get("2.0/repositories/{}/{}/src/{}/".format(input.workspace,
                                                             input.repository_slug,
                                                             input.branch_or_commit,
                                                             input.path),params=None)

    structure=client._get_objs(input.repository_slug, resp, params=None)

    return GetRepositoryStructureResponse(structure=structure)

# class File(BaseModel):
#     path: str
#     content: str
#
#     def to_file_request_input(self):
#         return (self.path, self.content)
#
#
# # TODO: uncomment after Bugfix: https://kubiya.atlassian.net/browse/PLAT-1123
# # class UploadFilesInput(BaseModel):
# #     workspace: str
# #     repository: str
# #     branch: str
# #     commit_message: str
# #     files: List[File]
#
#
# # @action_store.kubiya_action()
# # def upload_files(input: UploadFilesInput):
# #     client = get_client(input.workspace)
# #     res = client.post_repository_files(
# #         input.repository,
# #         input.commit_message,
# #         input.branch,
# #         files={file.path: file.to_file_request_input() for file in input.files},
# #     )
# #     return res
