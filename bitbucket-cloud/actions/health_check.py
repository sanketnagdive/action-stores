
import logging as log
from . import action_store
from ..bitbucket_client import Client
from .bitbucket_actions import get_client

def health_check():
    p = {
        "space": action_store.secrets["BITBUCKET_SPACE"],
        "user": action_store.secrets["BITBUCKET_USERNAME"],
        "pass": action_store.secrets["BITBUCKET_APP_PASSWORD"]
    }
    
    valid_user = param_check(p["user"])
    valid_pass = param_check(p["pass"])
    valid_space = param_check(p["sapce"])
    valid_user_login = user_login_check(p["token"])
    
    return valid_user | valid_pass | valid_space | valid_user_login

def param_check(param: str):
    return param is None or param == ""

def user_login_check(space: str):
    try:
        c = get_client(space)
        return c.get_user().login != ""
    except Exception as e:
        log.error("[error]", exception=str(e))
        return False


