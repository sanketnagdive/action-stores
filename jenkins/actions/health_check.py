import logging as log
from . import action_store
from .secrets import get_secrets
from .plugins import list_jenkins_plugins



@action_store.kubiya_action()
def health_check():
    host, user, pwd = get_secrets()
    return _param(host) and _param(user) and _param(pwd) and _conn()


def _conn() -> bool:
    try:
        resp = list_jenkins_plugins()
        return resp is not None and resp.status_code == 200
    except Exception as e:
        log.error("[error]", exception=str(e))
        return False


def _param(p: str) -> bool:
    return p is not None and p != ""


