import logging as log
from github import Github
from ..secrets import get_github_token, get_github_organization

def health_check():
    token = get_github_token()
    org = get_github_organization()
    
    return _param(org) & _param(token) & _user(token) & _org(token, org)

def _param(p: str):
    return p is None or p == ""

def _user(token: str):
    try:
        c = Github(token)
        return c.get_user().login != ""
    except Exception as e:
        log.error("[error]", exception=str(e))
        return False
    
def _org(token: str, org: str):
    try:
        c = Github(token)
        return c.get_organization(org).login != ""
    except Exception as e:
        log.error("[error]", exception=str(e))
        return False



