
import logging as log
from . import action_store
from .bitbucket_actions import get_client

def health_check():    
    space = action_store.secrets["BITBUCKET_SPACE"]
    user = action_store.secrets["BITBUCKET_USERNAME"]
    password = action_store.secrets["BITBUCKET_APP_PASSWORD"]
    return _param(user) & _param(password) & _param(space) & _user(space)

def _param(p: str):
    return p is None or p == ""

def _user(space: str):
    try:
        c = get_client(space)
        return c.get_user().login != ""
    except Exception as e:
        log.error("[error]", exception=str(e))
        return False
