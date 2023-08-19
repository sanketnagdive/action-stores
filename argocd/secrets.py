from . import action_store
import os

def get_user():
    return action_store.secrets.get("ARGO_USER")
def get_server():
    # return os.environ['ARGO_SERVER']
    return "https://argocd-server.argocd"
def get_password():
    return action_store.secrets.get("ARGO_PASS")