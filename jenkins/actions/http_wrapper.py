import requests
from .secrets import get_secrets

def get_wrapper(path: str):
    host, username, password = get_secrets()
    ret = requests.get(f"{host}/{path}", auth=(username, password))
    if not ret.ok:
        raise Exception(f"Error: {ret.status_code} {ret.text}")
    if ret.headers.get("Content-Type","").startswith("application/json"):
        return ret.json()
    else:
        return ret.text

    
def post_wrapper(endpoint: str, args: dict=None):
    host, username, password = get_secrets()
    ret = requests.post(f"{host}{endpoint}", auth=(username, password), data=args)
    if not ret.ok:
        raise Exception(f"Error: {ret.status_code} {ret.text}")
    if ret.headers.get("Content-Type","").startswith("application/json"):
        return ret.json()
    else:
        return ret.text