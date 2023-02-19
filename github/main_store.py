
import sys

from typing import Optional
from pathlib import Path
from pydantic import BaseModel
import kubiya
import requests



from typing import List, Dict, Any
import kubiya
from github import Github
from os import environ



store = kubiya.ActionStore("github", "0.2.0")
store.uses_secrets(["GITHUB_TOKEN", "GITHUB_ORGANIZATION"])

# orgprefix = orgname + "/"


def get_orgname(store):
    return store.secrets.get("GITHUB_ORGANIZATION", 'kubi-devops')

def get_orgprefix(store):
    return get_orgname(store) + "/"

def login(store) -> Github:
    return Github(store.secrets["GITHUB_TOKEN"])

@store.kubiya_action()
def list_org_repos(input=None) -> List[str]:
    orgname = get_orgname(store)
    repos = [
        repo.name
        for repo in login(store).get_organization(orgname).get_repos()
    ]
    return sorted(repos, key=lambda x:x.lower())

@store.kubiya_action()
def list_user_repos(username:str) -> List[str]:
    repos = [
        repo.name
        for repo in login(store).get_user(username).get_repos()
    ]
    return sorted(repos, key=lambda x:x.lower())

@store.kubiya_action()
def repo_details(params:Dict) -> Dict[str, Any]:
    orgprefix = get_orgprefix(store)
    repo_name = params["repo_name"]
    repo = login(store).get_repo(orgprefix + repo_name)
    return repo.raw_data

@store.kubiya_action()
def get_last_prs(params:Dict) -> List[Dict[str, Any]]:
    orgprefix = get_orgprefix(store)
    repo_name = params["repo_name"]
    limit = params.get("limit", 10)
    repo = login(store).get_repo(orgprefix + repo_name)
    return [
        {
            "user": pr.user.login,
            "title": pr.title,
            "number": pr.number,
            "created_at": pr.created_at.isoformat(),
            "head_branch": pr.head.ref,
            "target_branch": pr.base.ref,
         }
        for pr in repo.get_pulls(state='all')[:limit]
    ]

@store.kubiya_action()   
def get_open_prs(params:Dict) -> List[Dict[str, Any]]:
    orgprefix = get_orgprefix(store)
    repo_name = params["repo_name"]
    limit = params.get("limit", 10)
    state = params.get("state", "open")
    repo = login(store).get_repo(orgprefix + repo_name)
    return [
        {
            "user": pr.user.login,
            "title": pr.title,
            "number": pr.number,
            "created_at": pr.created_at.isoformat(),
            "head_branch": pr.head.ref,
            "target_branch": pr.base.ref,
         }
        for pr in repo.get_pulls(state='open')[:limit]
    ]

@store.kubiya_action()
def pr_details(params:Dict) -> Dict[str, Any]:
    orgprefix = get_orgprefix(store)
    repo_name = params["repo_name"]
    pr_number = params["pr_number"]
    repo = login(store).get_repo(orgprefix + repo_name)
    return repo.get_pull(number=pr_number).raw_data

@store.kubiya_action()
def merge_pr(params:Dict) -> Dict[str, Any]:
    orgprefix = get_orgprefix(store)
    repo_name = params["repo_name"]
    pr_number = params["pr_number"]
    repo = login(store).get_repo(orgprefix + repo_name)
    pr = repo.get_pull(number=pr_number)
    pr.merge()
    return pr.raw_data

@store.kubiya_action()
def approve_pr(params:Dict):
    orgprefix = get_orgprefix(store)
    repo_name = params["repo_name"]
    pr_number = params["pr_number"]
    repo = login(store).get_repo(orgprefix + repo_name)
    pr = repo.get_pull(number=pr_number)
    pr.approve()
    return pr.raw_data

@store.kubiya_action()
def last_commits(params:Dict) -> List[Dict[str, Any]]:
    orgprefix = get_orgprefix(store)
    repo_name = params["repo_name"]
    limit = params.get("limit", 20)
    repo = login(store).get_repo(orgprefix + repo_name)
    return [
        {
            "author": commit.author.login,
            "last_modified": commit.last_modified,
            "sha": commit.sha[:8],
        }
        for commit in repo.get_commits()[:limit]
    ]

@store.kubiya_action()
def commit_details(params:Dict) -> Dict[str, Any]:
    orgprefix = get_orgprefix(store)
    repo_name = params["repo_name"]
    sha = params["sha"]    
    repo = login(store).get_repo(orgprefix + repo_name)
    return repo.get_commit(sha).raw_data

@store.kubiya_action()
def list_workflows(params:Dict) -> List[Dict[str, Any]]:
    orgprefix = get_orgprefix(store)
    repo_name = params["repo_name"]
    repo = login(store).get_repo(orgprefix + repo_name)
    return [action.name for action in repo.get_workflows()]

@store.kubiya_action()
def last_workflow_runs(params:Dict) -> List[Dict[str, Any]]:
    orgprefix = get_orgprefix(store)
    repo_name = params["repo_name"]
    repo = login(store).get_repo(orgprefix + repo_name)
    limit = params.get("limit", 30)
    return [
        {
            "run_id": run.id,
            "status": run.status,
            "run_number": run.run_number,
            "created_at": run.created_at.isoformat(),
            "head_branch": run.head_branch,
        } for run in repo.get_workflow_runs()[:limit]
    ]

@store.kubiya_action()
def workflow_run_details(params:Dict) -> Dict[str, Any]:
    orgprefix = get_orgprefix(store)
    repo_name = params["repo_name"]
    run_id = params["run_id"]
    repo = login(store).get_repo(orgprefix + repo_name)
    return repo.get_workflow_run(run_id).raw_data


class Branch(BaseModel):
    name: str
    base: Optional[str]
    repo_name: str

@store.kubiya_action()
def create_branch(params: Branch):
    orgprefix = get_orgprefix(store)
    gh = login(store)
    repo = gh.get_repo(orgprefix + params.repo_name)
    branchname = params.name
    if params.base:
        basebranchname = params.base
    else:
        basebranchname = repo.default_branch
    basebranch = repo.get_branch(basebranchname)
    shafrom =  basebranch.commit.sha
    repo.create_git_ref(ref=f"refs/heads/{branchname}", sha=shafrom)
    return True

@store.kubiya_action()
def add_file_to_repo(params:Dict):
    orgprefix = get_orgprefix(store)
    gh = login(store)
    repo = gh.get_repo(orgprefix + params["repo_name"])
    basebranchname = params.get("branch", repo.default_branch)
    filepath = params["filepath"]
    filecontent = params["file"]
    commit_message = params.get("commit_message", "automated-commit by kubi")
    repo.create_file(path=filepath, message=commit_message, content=filecontent, branch=basebranchname)
    return filepath

class Pr(BaseModel):
    repo_name: str
    branch: str
    title: Optional[str]
    message: Optional[str]
    base: Optional[str]

@store.kubiya_action()  
def create_pr(params: Dict):
    orgprefix = get_orgprefix(store)
    gh = login(store)
    repo = gh.get_repo(orgprefix + params["repo_name"])
    title = params.get("title", "AutoPR by kubi")
    branch = params["branch"]
    body=params.get("message", "\n\n```auto pr by kubi```")
    basebranchname = params.get("base", repo.default_branch)
    repo.create_pull(base=basebranchname, title=title, head=branch, body=body)


@store.kubiya_action()
def get_repo_file_names(params: Dict) -> List[str]:
    orgprefix = get_orgprefix(store)
    gh = login(store)
    repo = gh.get_repo(orgprefix + params["repo_name"])
    branch = params.get("branch", repo.default_branch)

    return [
        t.path 
        for t in repo.get_git_tree(repo.get_branch(branch).commit.sha, recursive=True).tree
        if t.type == "blob"
    ]

@store.kubiya_action()
def get_repo_file(params: Dict):
    orgprefix = get_orgprefix(store)
    gh = login(store)
    repo = gh.get_repo(orgprefix + params["repo_name"])
    filepath = params["filepath"]
    branch = params.get("branch", repo.default_branch)
    return repo.get_contents(filepath, ref=branch).decoded_content


@store.kubiya_action()
def get_gist_files(params: Dict):
    gh = login(store)
    gist_id = params["id"]
    gist = gh.get_gist(gist_id)
    return {k: v.content for k,v in gist.files.items()}
