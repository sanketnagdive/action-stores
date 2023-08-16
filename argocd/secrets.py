from . import action_store

def get_user():
    return action_store.secrets.get("ARGO_USER")
def get_server():
    return action_store.secrets.get("ARGO_SERVER")
def get_password():
    return action_store.secrets.get("ARGO_PASS")