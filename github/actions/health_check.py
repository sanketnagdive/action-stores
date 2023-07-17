import logging as log
from .. import action_store
from ..github_wrapper import get_github_instance, get_entity
from ..secrets import get_github_token, get_github_organization


@action_store.kubiya_action()
def health_check():
    pwd = get_github_token()
    org = get_github_organization()
    return _param(org) and _param(pwd) and _conn(pwd=pwd, org=org)


def _param(p: str) -> bool:
    return p is not None and p != ""


def _conn(pwd: str, org: str) -> bool:
    try:
        c = get_entity(get_github_instance())
        return c.get_user().login != "" and c.get_organization(org).login != ""
    except Exception as e:
        log.error("[error]", exception=str(e))
        return False

