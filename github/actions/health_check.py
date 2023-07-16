import logging as log
from github import Github
from ..secrets import get_github_token, get_github_organization

def health_check():
    p = {
        "token": get_github_token(),
        "org": get_github_organization()
    }
    
    valid_org = param_check(p["org"])
    valid_token = param_check(p["token"])
    valid_user_login = user_login_check(p["token"])
    valid_org_login = org_login_check(p["token"], p["org"])
    
    return valid_org | valid_token | valid_user_login | valid_org_login

def param_check(param: str):
    return param is None or param == ""

def user_login_check(token: str):
    try:
        c = Github(token)
        return c.get_user().login != ""
    except Exception as e:
        log.error("[error]", exception=str(e))
        return False
    
def org_login_check(token: str, org: str):
    try:
        c = Github(token)
        return c.get_organization(org).login != ""
    except Exception as e:
        log.error("[error]", exception=str(e))
        return False



