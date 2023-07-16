import logging as log
from ..secrets import get_jira_secrets
from ..jira_wrapper import get_jira_instance


def health_check():
    url, user, pwd = get_jira_secrets()
    return _param(url) and _param(user) and _param(pwd) and _conn()


def _conn() -> bool:
    try:
        c = get_jira_instance()
        return c.myself()["accountId"] != ""
    except Exception as e:
        log.error("[error]", exception=str(e))
        return False


def _param(p: str) -> bool:
    return p is not None and p != ""

