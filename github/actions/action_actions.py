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
        resp = delete_wrapper(f"/repos/{params.owner}/{params.repo}/actions/artifacts/{params.artifact_id}")
        if resp['status'] == 204:
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
        response = get_wrapper(f"/repos/{params.owner}/{params.repo}/actions/artifacts/{params.run_id}/artifacts")
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
        response = delete_wrapper(f"/repos/{params.owner}/{params.repo}/actions/caches", data)
        return DeleteCachesByKeyResponse(resp=response)
    else:
        return FAILED_MSG

@action_store.kubiya_action()        
def delete_caches_by_id(params: DeleteCachesByIdParams) -> DeleteCachesByIdResponse:
    if params.dict(exclude_none = True):
        response = delete_wrapper(f"/repos/{params.owner}/{params.repo}/actions/caches/{params.cache_id}")
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
        resp = put_wrapper(f"/orgs/{params.org}/actions/oidc/customization/sub", data)
        if resp['status'] == 201:
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
        data.drop("owner")
        data.drop("repo")
        resp = put_wrapper(f"/orgs/{params.owner}/{params.repo}/actions/oidc/customization/sub", data)
        if resp['status'] == 201:
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


    

        