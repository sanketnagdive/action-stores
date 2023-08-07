from .secrets import get_bitbucket_username, get_bitbcuket_app_password
from .bitbucket_client import Client

from . import action_store


def get_client(workspace: str):
    return Client(
        user=get_bitbucket_username(),
        password=get_bitbcuket_app_password(),
        owner=workspace,
    )