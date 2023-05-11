from typing import List

from pydantic import BaseModel

from ..bitbucket_client import Client

from . import action_store


def get_client(workspace: str):
    return Client(
        user=action_store.secrets["BITBUCKET_USERNAME"],
        password=action_store.secrets["BITBUCKET_APP_PASSWORD"],
        owner=workspace,
    )


def get_attrs_from_dict(d: dict, attrs: list):
    return {k: d.get(k) for k in attrs}


class GetReposInput(BaseModel):
    workspace: str


@action_store.kubiya_action()
def get_repositories(input: GetReposInput):
    client = get_client(input.workspace)
    all_repos = client.all_pages(client.get_repositories)

    keys_to_return = [
        "name",
        "full_name",
        "description",
        "slug",
        "is_private",
        "uuid",
        "created_on",
        "updated_on",
        "size",
        "language",
        "has_issues",
        "has_wiki",
        "override_settings",
        "mainbranch",
    ]

    to_return = []
    for repo in all_repos:
        to_return.append(get_attrs_from_dict(repo, keys_to_return))

    return to_return


class GetRepositoryBranchesInput(BaseModel):
    workspace: str
    repository: str


@action_store.kubiya_action()
def get_repository_branches(input: GetRepositoryBranchesInput):
    client = get_client(input.workspace)
    all_branches = client.all_pages(client.get_repository_branches, input.repository)

    to_return = []
    for branch in all_branches:
        to_return.append(
            {
                "name": branch["name"],
                "author": branch["target"]["author"]["raw"],
                "merge_strategies": branch["merge_strategies"],
                "default_merge_strategy": branch["default_merge_strategy"],
            }
        )

    return to_return


class GetRepositoryStructureInput(BaseModel):
    workspace: str
    repository: str
    branch_or_commit: str


@action_store.kubiya_action()
def get_repository_structure(input: GetRepositoryStructureInput):
    client = get_client(input.workspace)
    all_files = client.get_repository_structure(
        input.repository, input.branch_or_commit
    )
    return all_files


class GetFileContentInput(BaseModel):
    workspace: str
    repository: str
    file_path: str
    commit_id: str


@action_store.kubiya_action()
def get_file_content(input: GetFileContentInput):
    client = get_client(input.workspace)
    file_content = client.get_repository_commit_path_source_code(
        input.repository, input.commit_id, input.file_path
    )
    return file_content


class CreatePRInput(BaseModel):
    workspace: str
    repository: str
    title: str
    source_branch: str
    destination_branch: str


@action_store.kubiya_action()
def create_pull_request(input: CreatePRInput):
    client = get_client(input.workspace)
    res = client.create_pull_request(
        input.repository,
        input.title,
        input.source_branch,
        input.destination_branch,
    )
    return res


class MergePRInput(BaseModel):
    workspace: str
    repository: str
    pull_request_id: str


@action_store.kubiya_action()
def merge_pull_request(input: MergePRInput):
    client = get_client(input.workspace)
    res = client.merge_pull_request(
        input.repository,
        input.pull_request_id,
    )
    return res


class GetOpenPullRequestsInput(BaseModel):
    workspace: str
    repository: str


@action_store.kubiya_action()
def get_open_pull_requests(input: GetOpenPullRequestsInput):
    client = get_client(input.workspace)
    res = list(client.all_pages(client.get_open_pull_requests, input.repository))
    return res


class File(BaseModel):
    path: str
    content: str

    def to_file_request_input(self):
        return (self.path, self.content)


class UploadFilesInput(BaseModel):
    workspace: str
    repository: str
    branch: str
    commit_message: str
    files: List[File]


@action_store.kubiya_action()
def upload_files(input: UploadFilesInput):
    client = get_client(input.workspace)
    res = client.post_repository_files(
        input.repository,
        input.commit_message,
        input.branch,
        files={file.path: file.to_file_request_input() for file in input.files},
    )
    return res
