from .secrets import get_bitbucket_username, get_bitbcuket_app_password
from .bitbucket_client import Client

from . import action_store


def get_client(workspace: str):
    return Client(
        user=action_store.secrets.get("BITBUCKET_USERNAME"),
        password=action_store.secrets.get("BITBUCKET_APP_PASSWORD"),
        owner=workspace,
    )