from typing import List, Any
import requests
from kubiya import ActionStore

actions_store = ActionStore("jenkins", version="0.2.0")

def get_secrets():
    host = actions_store.secrets.get("JENKINS_URL")
    username = actions_store.secrets.get("JENKINS_USER")
    password = actions_store.secrets.get("JENKINS_PASSWORD")
    return host, username, password

def get_wrapper(path: str):
    host, username, password = get_secrets()
    ret = requests.get(f"{host}/{path}", auth=(username, password))
    if not ret.ok:
        raise Exception("Error: {ret.status_code} {ret.text}")
    if ret.headers.get("Content-Type","").startswith("application/json"):
        return ret.json()
    else:
        return ret.text

    
def post_wrapper(endpoint: str, args: dict=None):
    host, username, password = get_secrets()
    ret = requests.post(f"{host}{endpoint}", auth=(username, password), data=args)
    if not ret.ok:
        raise Exception(f"Error: {ret.status_code} {ret.text}")
    if ret.headers.get("Content-Type","").startswith("application/json"):
        return ret.json()
    else:
        return ret.text

def text_in_log_output(log_output: str, text: str):
    return text in log_output
    
@actions_store.kubiya_action()
def get_all_jobs(_:Any=None) -> List:
    return get_wrapper("/api/json?tree=jobs[name,url]")

@actions_store.kubiya_action()
def get_job_data(params: dict):
    return get_wrapper(f"/job/{params['job_name']}/api/json")

@actions_store.kubiya_action()
def get_job_params(params: dict):
    return get_wrapper(f"/job/{params['job_name']}/api/json?tree=actions[parameterDefinitions[name,type,choices]]")

@actions_store.kubiya_action()
def build_job(params: dict):
    job_name = params.pop("job_name")
    if params:
        post_wrapper(f"/job/{job_name}/buildWithParameters", params)
    else:
        post_wrapper(f"/job/{job_name}/build")
    return f"Building job {job_name} with args {params}"

@actions_store.kubiya_action()
def get_builds(params: dict):
    return get_wrapper(f"job/{params['job_name']}/api/json?tree=builds[id,url,timestamp,result,duration]")

# @actions_store.kubiya_action()
# def get_build_console(params: dict):
#     return get_wrapper(f"job/{params['job_name']}/{params['build_number']}/consoleText").splitLines()

@actions_store.kubiya_action()
def text_in_build_log(params: dict):
    log_output = get_wrapper(f"job/{params['job_name']}/{params['build_number']}/consoleText")
    return text_in_log_output(log_output, params["text"])

@actions_store.kubiya_action()
def filter_text_in_build_log(params: dict):
    log_output = get_wrapper(f"job/{params['job_name']}/{params['build_number']}/consoleText")
    return [line for line in log_output.splitlines() if text_in_log_output(line, params["text"])]

@actions_store.kubiya_action()
def get_build_url(params: dict):
    return get_wrapper(f"job/{params['job_name']}/{params['build_number']}/api/json?tree=url")["url"]

@actions_store.kubiya_action()
def get_build_data(params: dict):
    return get_wrapper(f"job/{params['job_name']}/{params['build_number']}/api/json")

@actions_store.kubiya_action()
def get_last_build(params: dict):
    return get_wrapper(f"job/{params['job_name']}/api/json?tree=lastBuild[id,url,timestamp,result,duration]")

@actions_store.kubiya_action()
def get_all_builds(params: dict):
    return get_wrapper(f"job/{params['job_name']}/api/json")

@actions_store.kubiya_action()
def list_builds(params: dict):
    return get_wrapper(f"job/{params['job_name']}/api/json?tree=builds[number,timestamp,result,duration]")

@actions_store.kubiya_action()
def get_build_status(params: dict):
    return get_wrapper(f"job/{params['job_name']}/lastBuild/api/json?tree=result")

@actions_store.kubiya_action()
def stop_job(params: dict):
    return post_wrapper(f"job/{params['job_name']}/lastBuild/stop")

@actions_store.kubiya_action()
def get_jenkins_logs(params: dict):
    return get_wrapper(f"/job/{params['job_name']}/{params['jenkins_number']}/consoleText")

actions_store.uses_secrets(["JENKINS_URL", "JENKINS_PASSWORD", "JENKINS_USER"])

actions_store.register_action("get_jenkins_host", lambda x: actions_store.secrets.get("JENKINS_URL"))