from .. import action_store as action_store
import logging
from ..models.actions import *
from ..http_wrapper import get_wrapper, post_wrapper, patch_wrapper, delete_wrapper, put_wrapper

FAILED_MSG = "Insufficient data"

@action_store.kubiya_action()
def list_repo_artifacts(params: ListRepoArtifactsParams) -> ListRepoArtifactsResponse:
    data = params.dict(exclude_none = True)
    if data:
        data.pop("owner")
        data.pop("repo")
        response = get_wrapper(f"/repos/{params.owner}/{params.repo}/actions/artifacts", data)
        return ListRepoArtifactsResponse(resp=response)
    else:
        return FAILED_MSG

@action_store.kubiya_action()
def get_artifact(params: GetArtifactParams) -> GetArtifactResponse:
    data = params.dict(exclude_none = True)
    if data:
        response = get_wrapper(f"/repos/{params.owner}/{params.repo}/actions/artifacts/{params.artifact_id}")
        return GetArtifactResponse(resp=response)
    else:
        return FAILED_MSG
    
@action_store.kubiya_action()
def delete_artifact(params:DeleteArtifactParams):
    if params.dict(exclude_none = True):
        _, status = delete_wrapper(f"/repos/{params.owner}/{params.repo}/actions/artifacts/{params.artifact_id}")
        if status == 204:
            return f"Artifact with id {params.artifact_id} successfully deleted"
        else:
            return "Process failed."
    else:
        return FAILED_MSG
    
@action_store.kubiya_action()
def download_artifact(params:DownloadArtifactParams):
    if params.dict(exclude_none = True):
        resp = get_wrapper(f"/repos/{params.owner}/{params.repo}/actions/artifacts/{params.artifact_id}/{params.archive_format}")
        if resp['status'] == 302:
            return f"Artifact with id {params.artifact_id} successfully downloaded"
        else:
            return "Process failed."
    else:
        return FAILED_MSG
    
@action_store.kubiya_action()
def list_workflow_run_artifacts(params: ListWorkflowRunArtifactsParams) -> ListWorkflowRunArtifactsResponse:
    if params.dict(exclude_none = True):
        response = get_wrapper(f"/repos/{params.owner}/{params.repo}/actions/runs/{params.run_id}/artifacts")
        return ListWorkflowRunArtifactsResponse(resp=response)
    else:
        return FAILED_MSG
    
@action_store.kubiya_action()    
def get_org_cache_usage(params: GetOrgCacheUsageParams) -> GetOrgCacheUsageResponse:
    if params.dict(exclude_none = True):
        response = get_wrapper(f"/orgs/{params.org}/actions/cache/usage")
        return GetOrgCacheUsageResponse(resp=response)
    else:
        return FAILED_MSG
    
@action_store.kubiya_action()    
def list_repos_with_cache_usage_by_org(params: ListReposWithCacheUsageInOrgParams) -> ListReposWithCacheUsageInOrgResponse:
    data =  params.dict(exclude_none = True)
    if data:
        data.pop("org")
        response = get_wrapper(f"/orgs/{params.org}/actions/cache/usage-by-repository", data)
        return ListReposWithCacheUsageInOrgResponse(resp=response)
    else:
        return FAILED_MSG

@action_store.kubiya_action()        
def get_repo_cache_usage(params: GetRepoCacheUsageParams) -> GetRepoCacheUsageResponse:
    if params.dict(exclude_none = True):
        response = get_wrapper(f"/repos/{params.owner}/{params.repo}/actions/cache/usage")
        return GetRepoCacheUsageResponse(resp=response)
    else:
        return FAILED_MSG
    
@action_store.kubiya_action()        
def list_caches_in_repo(params: ListCachesInRepoParams) -> ListCachesInRepoResponse:
    data = params.dict(exclude_none = True)
    if data:
        data.pop("owner")
        data.pop("repo")
        response = get_wrapper(f"/repos/{params.owner}/{params.repo}/actions/caches", data)
        return ListCachesInRepoResponse(resp = response)
    else:
        return FAILED_MSG

@action_store.kubiya_action()        
def delete_caches_by_key(params: DeleteCachesByKeyParams) -> DeleteCachesByKeyResponse:
    data = params.dict(exclude_none=True)
    if data:
        data.pop("owner")
        data.pop("repo")
        response, _ = delete_wrapper(f"/repos/{params.owner}/{params.repo}/actions/caches", data)
        return DeleteCachesByKeyResponse(resp=response)
    else:
        return FAILED_MSG

@action_store.kubiya_action()        
def delete_caches_by_id(params: DeleteCachesByIdParams) -> DeleteCachesByIdResponse:
    if params.dict(exclude_none = True):
        response, _ = delete_wrapper(f"/repos/{params.owner}/{params.repo}/actions/caches/{params.cache_id}")
        return DeleteCachesByIdResponse(resp = response)
    else:
        return FAILED_MSG
    
@action_store.kubiya_action() 
def get_oidc_sc_customization_template_by_org(params: GetCustomizationTemplateForOIDCSubjectClaimOrgParams) -> GetCustomizationTemplateForOIDCSubjectClaimOrgResponse:
    if params.dict(exclude_none = True):
        response = get_wrapper(f"/orgs/{params.org}/actions/oidc/customization/sub")
        return GetCustomizationTemplateForOIDCSubjectClaimOrgResponse(resp=response)
    else:
        return FAILED_MSG

@action_store.kubiya_action()     
def set_oidc_sc_customization_template_by_org(params: SetCustomizationTemplateForOIDCSubjectClaimOrgParams):
    data = params.dict(exclude_none = True)
    if data:
        data.pop("org")
        _, status = put_wrapper(f"/orgs/{params.org}/actions/oidc/customization/sub", data)
        if status == 201:
            return f"Customization template for org {params.org} successfully set."
        else:
            return "Operation failed"
    else:
        return FAILED_MSG

@action_store.kubiya_action()     
def get_oidc_sc_customization_template_by_repo(params: GetCustomizationTemplateForOIDCSubjectClaimRepoParams) -> GetCustomizationTemplateForOIDCSubjectClaimRepoResponse:
    if params.dict(exclude_none = True):
        response = get_wrapper(f"/orgs/{params.owner}/{params.repo}/actions/oidc/customization/sub")
        return GetCustomizationTemplateForOIDCSubjectClaimRepoResponse(resp=response)
    else:
        return FAILED_MSG

@action_store.kubiya_action()     
def set_oidc_sc_customization_template_by_repo(params: SetCustomizationTemplateForOIDCSubjectClaimRepoParams):
    data = params.dict(exclude_none = True)
    if data:
        data.pop("owner")
        data.pop("repo")
        _, status = put_wrapper(f"/orgs/{params.owner}/{params.repo}/actions/oidc/customization/sub", data)
        if status == 201:
            return f"Customization template for repo {params.repo} successfully set."
        else:
            return "Operation failed"
    else:
        return FAILED_MSG
    
@action_store.kubiya_action() 
def get_actions_permissions_by_org(params: GetOrgsActionsPermissionsParams) -> GetOrgsActionsPermissionsResponse:
    if params.dict(exclude_none = True):
        response = get_wrapper(f"/orgs/{params.org}/actions/permissions")
        return GetOrgsActionsPermissionsResponse(resp=response)
    else:
        return FAILED_MSG

@action_store.kubiya_action() 
def set_actions_permissions_by_org(params: SetOrgsActionsPermissionsParams):
    data = params.dict(exclude_none = True)
    if data:
        data.pop("org")
        _, status = put_wrapper(f"/orgs/{params.org}/actions/permissions", data)
        if status == 204:
            return f"Actions permissions successfully set"
        else:
            return "Operation failed"
    else:
        return FAILED_MSG

@action_store.kubiya_action()     
def list_selected_repos_with_actions_by_org(params: ListSelectedReposEnabledForActionsByOrgParams) -> ListSelectedReposEnabledForActionsByOrgResponse:
    if params.dict(exclude_none = True):
        response = get_wrapper(f"/orgs/{params.org}/actions/permissions/repositories")
        return ListSelectedReposEnabledForActionsByOrgResponse(resp=response)
    else:
        return FAILED_MSG

@action_store.kubiya_action()     
def set_repos_enabled_for_actions_by_org(params: SetReposEnabledForActionsByOrgParams):
    data = params.dict(exclude_none = True)
    if data:
        data.pop("org")
        _, status = put_wrapper(f"/orgs/{params.org}/actions/permissions/repositories", data)
        if status == 204:
            return f"Actions permissions successfully set"
        else:
            return "Operation failed"
    else:
        return FAILED_MSG

@action_store.kubiya_action()     
def enable_repo_in_org_for_actions(params: EnableRepoInOrgForActionsParams):
    if params.dict(exclude_none = True):
        _, status = put_wrapper(f"/orgs/{params.org}/actions/permissions/repositories/{params.repository_id}")
        if status == 204:
            return f"Repository {params.repository_id} enabled"
        else:
            return "Operation failed"
    else:
        return FAILED_MSG

@action_store.kubiya_action()     
def disable_repo_in_org_for_actions(params: DisableRepoInOrgForActionsParams):
    if params.dict(exclude_none = True):
        _, status = delete_wrapper(f"/orgs/{params.org}/actions/permissions/repositories/{params.repository_id}")
        if status == 204:
            return f"Repository {params.repository_id} disabled"
        else:
            return "Operation failed"
    else:
        return FAILED_MSG

@action_store.kubiya_action()     
def get_allowed_actions_for_org(params: GetAllowedActionsByOrgParams) -> GetAllowedActionsByOrgResponse:
    if params.dict(exclude_none = True):
        response = get_wrapper(f"/orgs/{params.org}/actions/permissions/selected-actions")
        return GetAllowedActionsByOrgResponse(resp=response)
    else:
        return FAILED_MSG

@action_store.kubiya_action()     
def set_allowed_actions_for_org(params: SetAllowedActionsByOrgParams):
    data = params.dict(exclude_none = True)
    if data:
        data.pop("org")
        _, status = put_wrapper(f"/orgs/{params.org}/actions/permissions/selected-actions", data)
        if status == 204:
            return f"Allowed actions for organization {params.org} set"
        else:
            return "Operation failed"
    else:
        return FAILED_MSG

@action_store.kubiya_action()
def list_org_secrets(params: ListOrgSecretsParams) -> ListOrgSecretsResponse:
    if params.dict(exclude_none = True):
        response = get_wrapper(f"/orgs/{params.org}/actions/secrets")
        return ListOrgSecretsResponse(resp=response)
    else:
        return FAILED_MSG

@action_store.kubiya_action()
def get_org_public_key(params: GetOrgPublicKeyParams) -> GetOrgPublicKeyResponse:
    if params.dict(exclude_none = True):
        response = get_wrapper(f"/orgs/{params.org}/actions/secrets/public-key")
        return GetOrgPublicKeyResponse(resp=response)
    else:
        return FAILED_MSG

@action_store.kubiya_action()    
def get_org_secret(params: GetOrgSecretParams) -> GetOrgSecretResponse:
    if params.dict(exclude_none = True):
        response = get_wrapper(f"/orgs/{params.org}/actions/secrets/{params.secret_name}")
        return GetOrgSecretResponse(resp = response)
    else:
        return FAILED_MSG

@action_store.kubiya_action()    
def create_update_org_secret(params: CreateUpdateOrgSecretParams):
    data = params.dict(exclude_none = True)
    if data:
        data.pop("org")
        data.pop("secret_name")
        data['key_id'] = get_wrapper(f'/orgs/{params.org}/actions/secrets/public-key')['key_id']
        _, status = put_wrapper(f"/orgs/{params.org}/actions/secrets/{params.secret_name}", data)
        if status == 201:
            return f"Updated secret {params.secret_name} successfully"
        elif status == 204:
            return f"Created secret {params.secret_name} successfully"
        else:
            return "Operation failed"
    else:
        return FAILED_MSG

@action_store.kubiya_action()    
def delete_org_secret(params: DeleteOrgSecretParams):
    if params.dict(exclude_none = True):
        _, status = delete_wrapper(f"/orgs/{params.org}/actions/secrets/{params.secret_name}")
        if status == 204:
            return f"Deleted secret {params.secret_name}"
        else:
            return "Operation failed"
    else:
        return FAILED_MSG
    
@action_store.kubiya_action()    
def list_repo_secrets(params: ListRepoSecretsParams) -> ListRepoSecretsResponse:
    if params.dict(exclude_none = True):
        response = get_wrapper(f"/repos/{params.owner}/{params.repo}/actions/secrets")
        return ListRepoSecretsResponse(resp=response)
    else:
        return FAILED_MSG

@action_store.kubiya_action()    
def get_repo_public_key(params: GetRepoPublicKeyParams) -> GetRepoPublicKeyResponse:
    if params.dict(exclude_none = True):
        response = get_wrapper(f"/repos/{params.owner}/{params.repo}/actions/secrets/public-key")
        return GetRepoPublicKeyResponse(resp=response)
    else:
        return FAILED_MSG

@action_store.kubiya_action()    
def get_repo_secret(params: GetRepoSecretParams) -> GetRepoSecretResponse:
    if params.dict(exclude_none = True):
        response = get_wrapper(f"/repos/{params.owner}/{params.repo}/actions/secrets/{params.secret_name}")
        return GetRepoSecretResponse(resp=response)
    else:
        return FAILED_MSG

@action_store.kubiya_action()   
def create_update_repo_secret(params: CreateUpdateRepoSecretParams):
    data = params.dict(exclude_none=True)
    if data:
        data.pop("owner")
        data.pop("repo")
        data.pop("secret_name")
        data['key_id'] = get_wrapper(f"/repos/{params.owner}/{params.repo}/actions/secrets/public-key")['key_id']
        if len(data) == 0:
            data = None
        _, status = put_wrapper(f"/repos/{params.owner}/{params.repo}/actions/secrets/{params.secret_name}", data)
        if status == 201:
            return f"Created secret {params.secret_name} successfully"
        else:
            return "Operation failed"
    else:
        return FAILED_MSG

@action_store.kubiya_action()    
def delete_repo_secret(params: DeleteRepoSecretParams):
    if params.dict(exclude_none = True):
        _, status = delete_wrapper(f"/repos/{params.owner}/{params.repo}/actions/secrets/{params.secret_name}")
        if status == 204:
            return f"Deleted secret {params.secret_name}"
        else:
            return "Operation failed"
    else:
        return FAILED_MSG
    


    

        