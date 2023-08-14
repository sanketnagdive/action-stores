from typing import List

from pydantic import BaseModel


from .. import action_store
from .. bitbucket_wrapper import get_client

from ..models.pipelines import (
    GetPipelineRequest,GetPipelineResponse,
    GetPipelinesRequest,GetPipelinesResponse,
    RunPipelineRequest,RunPipelineResponse,
    StopPipelineRequest,StopPipelineResponse,
)


# @action_store.kubiya_action()
def get_pipeline(input: GetPipelineRequest )->GetPipelineResponse:
    client = get_client(input.workspace)
    pipelines = client._get("2.0/repositories/{}/{}/pipelines/{}".format(input.workspace,
                                                                         input.repo_slug,
                                                                         input.pipeline_uuid),params=None,)

    return GetPipelineResponse(pipelines=pipelines)

@action_store.kubiya_action()
def get_pipelines(input: GetPipelinesRequest )->GetPipelinesResponse:
    client = get_client(input.workspace)
    pipelines = client._get("2.0/repositories/{}/{}/pipelines".format(input.workspace,
                                                                      input.repo_slug),params=None,)

    return GetPipelinesResponse(pipelines=pipelines)


@action_store.kubiya_action()
def run_pipeline(input: RunPipelineRequest )->RunPipelineResponse:
    client = get_client(input.workspace)
    response = client._post("2.0/repositories/{}/{}/pipelines/".format(input.workspace,
                                                                       input.repo_slug),
                            data={
                                "target": {
                                    "type": "pipeline_ref_target",
                                    "ref_type": "branch",
                                    "ref_name": input.branch_name  # Replace with the branch you want to trigger the pipeline for
                                }},params=None,)

    return RunPipelineResponse(run=response)

@action_store.kubiya_action()
def stop_pipeline(input: StopPipelineRequest )->StopPipelineResponse:
    client = get_client(input.workspace)
    response= client._post("2.0/repositories/{}/{}/pipelines/{}/stopPipeline".format(input.workspace,
                                                                                     input.repo_slug,
                                                                                     input.pipeline_uuid,
                                                                                     input.run_uuid),params=None,)

    # # Check if the response status code is 204 (the base client returns empty string for 204 responses)
    if response == '':
    # If it's a 204 response, return an empty dictionary
        return StopPipelineResponse(run={})
