from typing import List, Any, Optional
from pydantic import BaseModel
from . import action_store as action_store
from .http_wrapper import get_wrapper, post_wrapper

class JenkinsJob(BaseModel):
    name: str
    url: str

class JenkinsBuild(BaseModel):
    id: str
    url: str
    timestamp: int
    result: str
    duration: int

class JenkinsBuildLog(BaseModel):
    log: str

class JobParams(BaseModel):
    job_name: str

class BuildParams(BaseModel):
    job_name: str
    build_number: str

class TextSearchParams(BaseModel):
    job_name: str
    build_number: str
    text: str

class NewJobConfig(BaseModel):
    job_name: str
    config_xml: str

class JenkinsJob(BaseModel):
    name: str
    url: str

class JobDeleteParams(BaseModel):
    job_name: str

class JobParamsRequest(BaseModel):
    job_name: str


class JobParameter(BaseModel):
    name: str
    type: str
    choices: List[str]


class JobParamsResponse(BaseModel):
    parameters: List[JobParameter]

class BuildConsoleLogsRequest(BaseModel):
    job_name: str
    build_number: int


class BuildConsoleLogsResponse(BaseModel):
    console_logs: str

class TriggerJobRequest(BaseModel):
    job_name: str
    parameters: Optional[dict] = None

class TriggerJobResponse(BaseModel):
    success: bool
    message: str

class CancelJobRequest(BaseModel):
    job_name: str

class CancelJobResponse(BaseModel):
    success: bool
    message: str

class JobStatusRequest(BaseModel):
    job_name: str

class JobStatusResponse(BaseModel):
    status: str
    message: str

@action_store.kubiya_action()
def get_job_status(request: JobStatusRequest) -> JobStatusResponse:
    endpoint = f"/job/{request.job_name}/lastBuild/api/json?tree=result"
    try:
        response = get_wrapper(endpoint)
        status = response["result"]
        message = "Job is in progress."
        if status in ["SUCCESS", "FAILURE"]:
            message = f"Job status: {status}"
        return JobStatusResponse(status=status, message=message)
    except Exception as e:
        return JobStatusResponse(status="", message=str(e))

@action_store.kubiya_action()
def cancel_job(request: CancelJobRequest) -> CancelJobResponse:
    endpoint = f"/job/{request.job_name}/lastBuild/stop"
    try:
        post_wrapper(endpoint)
        return CancelJobResponse(success=True, message="Job canceled successfully.")
    except Exception as e:
        return CancelJobResponse(success=False, message=str(e))

@action_store.kubiya_action()
def trigger_job(request: TriggerJobRequest) -> TriggerJobResponse:
    endpoint = f"/job/{request.job_name}/buildWithParameters" if request.parameters else f"/job/{request.job_name}/build"
    try:
        post_wrapper(endpoint, request.parameters)
        return TriggerJobResponse(success=True, message="Job triggered successfully.")
    except Exception as e:
        return TriggerJobResponse(success=False, message=str(e))

@action_store.kubiya_action()
def get_build_console_logs(request: BuildConsoleLogsRequest) -> BuildConsoleLogsResponse:
    job_name = request.job_name
    build_number = request.build_number
    console_logs_endpoint = f"/job/{job_name}/{build_number}/consoleText"
    console_logs = get_wrapper(console_logs_endpoint)

    return BuildConsoleLogsResponse(console_logs=console_logs)

@action_store.kubiya_action()
def get_job_params(request: JobParamsRequest) -> JobParamsResponse:
    job_name = request.job_name
    params_endpoint = f"/job/{job_name}/api/json?tree=actions[parameterDefinitions[name,type,choices]]"
    response = get_wrapper(params_endpoint)

    parameters = []
    if "actions" in response:
        actions = response["actions"]
        for action in actions:
            if "parameterDefinitions" in action:
                parameter_definitions = action["parameterDefinitions"]
                for parameter_definition in parameter_definitions:
                    name = parameter_definition["name"]
                    param_type = parameter_definition["type"]
                    choices = parameter_definition.get("choices", [])
                    parameter = JobParameter(name=name, type=param_type, choices=choices)
                    parameters.append(parameter)

    return JobParamsResponse(parameters=parameters)

@action_store.kubiya_action()
def delete_job(params: JobDeleteParams):
    job_name = params.job_name
    delete_endpoint = f"/job/{job_name}/doDelete"
    response = post_wrapper(delete_endpoint)
    return f"Deleted job: {job_name}"

@action_store.kubiya_action()
def get_all_jobs(_: Any = None) -> List[JenkinsJob]:
    response = get_wrapper("/api/json?tree=jobs[name,url]")
    if response:
        return [JenkinsJob(name=job["name"], url=job["url"]) for job in response["jobs"]]
    else:
        return []

@action_store.kubiya_action()
def get_all_jobs(_: Any = None) -> List[JenkinsJob]:
    return get_wrapper("/api/json?tree=jobs[name,url]")

@action_store.kubiya_action()
def get_job_data(params: JobParams) -> dict:
    return get_wrapper(f"/job/{params.job_name}/api/json")

@action_store.kubiya_action()
def get_job_params(params: JobParams) -> dict:
    return get_wrapper(f"/job/{params.job_name}/api/json?tree=actions[parameterDefinitions[name,type,choices]]")

@action_store.kubiya_action()
def build_job(params: JobParams) -> str:
    if params.dict():
        post_wrapper(f"/job/{params.job_name}/buildWithParameters", params.dict())
    else:
        post_wrapper(f"/job/{params.job_name}/build")
    return f"Building job {params.job_name} with args {params.dict()}"

@action_store.kubiya_action()
def get_builds(params: JobParams) -> List[JenkinsBuild]:
    return get_wrapper(f"job/{params.job_name}/api/json?tree=builds[id,url,timestamp,result,duration]")

@action_store.kubiya_action()
def get_build_console(params: BuildParams) -> JenkinsBuildLog:
    log_output = get_wrapper(f"job/{params.job_name}/{params.build_number}/consoleText")
    return JenkinsBuildLog(log=log_output)

@action_store.kubiya_action()
def text_in_build_log(params: TextSearchParams) -> bool:
    log_output = get_wrapper(f"job/{params.job_name}/{params.build_number}/consoleText")
    return params.text in log_output

@action_store.kubiya_action()
def filter_text_in_build_log(params: TextSearchParams) -> List[str]:
    log_output = get_wrapper(f"job/{params.job_name}/{params.build_number}/consoleText")
    return [line for line in log_output.splitlines() if params.text in line]

@action_store.kubiya_action()
def get_build_url(params: BuildParams) -> str:
    return get_wrapper(f"job/{params.job_name}/{params.build_number}/api/json?tree=url")["url"]

@action_store.kubiya_action()
def get_build_data(params: BuildParams) -> dict:
    return get_wrapper(f"job/{params.job_name}/{params.build_number}/api/json")

@action_store.kubiya_action()
def get_last_build(params: JobParams) -> JenkinsBuild:
    return get_wrapper(f"job/{params.job_name}/api/json?tree=lastBuild[id,url,timestamp,result,duration]")

@action_store.kubiya_action()
def get_all_builds(params: JobParams) -> dict:
    return get_wrapper(f"job/{params.job_name}/api/json")

@action_store.kubiya_action()
def list_builds(params: JobParams) -> List[JenkinsBuild]:
    return get_wrapper(f"job/{params.job_name}/api/json?tree=builds[number,timestamp,result,duration]")

@action_store.kubiya_action()
def get_build_status(params: JobParams) -> dict:
    return get_wrapper(f"job/{params.job_name}/lastBuild/api/json?tree=result")

@action_store.kubiya_action()
def stop_job(params: JobParams) -> dict:
    return post_wrapper(f"job/{params.job_name}/lastBuild/stop")

@action_store.kubiya_action()
def get_jenkins_logs(params: BuildParams) -> JenkinsBuildLog:
    log_output = get_wrapper(f"/job/{params.job_name}/{params.build_number}/consoleText")
    return JenkinsBuildLog(log=log_output)