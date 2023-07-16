import logging as log
from ..github_wrapper import get_github_instance, get_entity
from ..secrets import get_github_token, get_github_organization


def health_check():
    pwd = get_github_token()
    org = get_github_organization()
    return _param(org) & _param(pwd) & _conn(pwd=pwd, org=org)


def _param(p: str) -> bool:
    return p is not None & p != ""


def _conn(pwd: str, org: str) -> bool:
    try:
        c = get_entity(get_github_instance())
        return c.get_user().login != "" & c.get_organization(org).login != ""
    except Exception as e:
        log.error("[error]", exception=str(e))
        return False

