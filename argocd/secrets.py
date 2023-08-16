from . import action_store



def get_user():
    return os.environ.get("ARGO_USER", "michael")

def get_server():
    return os.environ.get("ARGO_SERVER", "https://argocd-int.dev.kubiya.ai/")

def get_password():
    return action_store.secrets.get("ARGO_PASS")