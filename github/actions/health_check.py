import logging as log
from github import Github
from .. import action_store

def health_check():
    p = {
        "token": action_store.secrets.get("GITHUB_TOKEN"),
        "org": action_store.secrets.get("GITHUB_ORGANIZATION")
    }
    
    valid_org = org_check(p["org"])
    valid_token = token_check(p["token"])
    valid_user_login = user_login_check(p["token"])
    valid_org_login = org_login_check(p["token"], p["org"])
    
    return valid_org | valid_token | valid_user_login | valid_org_login

def org_check(org: str):
    return org is None or org == ""

def token_check(token: str):
    return token is None or token == ""

def user_login_check(token: str):
    try:
        g = Github(token)
        return g.get_user().login != ""
    except Exception as e:
        log.error("[error]", exception=str(e))
        return False
    
def org_login_check(token: str, org: str):
    try:
        g = Github(token)
        return g.get_organization(org).login != ""
    except Exception as e:
        log.error("[error]", exception=str(e))
        return False



