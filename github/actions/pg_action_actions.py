from github import GithubException, UnknownObjectException, ContentFile
import logging
from ..github_wrapper import get_github_instance, get_entity
from ..models.actions import *
from .. import action_store as action_store

logger = logging.getLogger(__name__)

@action_store.kubiya_action()
def list_repo_artifacts(params: ListRepoArtifactsParams) -> ListRepoArtifactsResponse:
    try:
        github = get_github_instance()
        entity = get_entity(github)
        repo = entity.get_repo(params.repo)
        response = repo.get_artifacts()
        return ListRepoArtifactsResponse(resp=response)
    except GithubException as e:
        logger.error(f"Failed to get artifact list")


@action_store.kubiya_action()
def get_artifact(params: GetArtifactParams) -> GetArtifactResponse:
    try:
        github = get_github_instance()
        entity = get_entity(github)
        repo = entity.get_repo(params.repo)
        response = repo.get_artifact(params.artifact_id)
        return GetArtifactResponse(resp=response)
    except GithubException as e:
        logger.error(f"Failed to get artifact: {e}")

@action_store.kubiya_action()
def delete_artifact(params:DeleteArtifactParams):
    try:
        github = get_github_instance()
        entity = get_entity(github)
        repo = entity.get_repo(params.repo)
        artifact = repo.get_artifact(params.artifact_id)
        response = artifact.delete()
        return GetArtifactResponse(resp=response)
    except GithubException as e:
        logger.error(f"Failed to get artifact: {e}")
