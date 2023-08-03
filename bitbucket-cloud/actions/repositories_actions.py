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


# class GetRepositoryStructureInput(BaseModel):
#     workspace: str
#     repository: str
#     branch_or_commit: str
#
#
# @action_store.kubiya_action()
# def get_repository_structure(input: GetRepositoryStructureInput):
#     client = get_client(input.workspace)
#     all_files = client.get_repository_structure(
#         input.repository, input.branch_or_commit
#     )
#     return all_files



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
#
#
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
#
#
# class UploadFileInput(BaseModel):
#     workspace: str
#     repository: str
#     branch: str
#     commit_message: str
#     file_path: str
#     file_content: str
#
#
# @action_store.kubiya_action()
# def upload_file(input: UploadFileInput):
#     client = get_client(input.workspace)
#     res = client.post_repository_files(
#         input.repository,
#         input.commit_message,
#         input.branch,
#         files={input.file_path: input.file_content},
#     )
#     return res
