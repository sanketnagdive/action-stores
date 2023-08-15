import requests
from .secrets import get_secrets
import json

def get_wrapper(path: str, args: dict = None):
    token = get_secrets()
    headers = {"Authorization": "token {}".format(token)}
    ret = requests.get(f"https://api.github.com{path}", headers=headers, data=json.dumps(args))
    if not ret.ok:
        raise Exception(f"Error: {ret.status_code} {ret.text}")
    if ret.headers.get("Content-Type","").startswith("application/json"):
        return ret.json()
    else:
        return ret.text
    
def post_wrapper(path: str, args: dict=None):
    token = get_secrets()
    headers = {"Authorization": "token {}".format(token)}
    ret = requests.post(f"https://api.github.com{path}", headers=headers, data=json.dumps(args))
    if not ret.ok:
        raise Exception(f"Error: {ret.status_code} {ret.text}")
    if ret.headers.get("Content-Type","").startswith("application/json"):
        return ret.json()
    else:
        return ret.text

def patch_wrapper(path: str, args: dict=None):
    token = get_secrets()
    headers = {"Authorization": "token {}".format(token)}
    ret = requests.post(f"https://api.github.com{path}", headers=headers, data=json.dumps(args))
    if not ret.ok:
        raise Exception(f"Error: {ret.status_code} {ret.text}")
    if ret.headers.get("Content-Type","").startswith("application/json"):
        return ret.json()
    else:
        return ret.text
    
def delete_wrapper(path: str, args: dict=None):
    token = get_secrets()
    headers = {"Authorization": "token {}".format(token)}
    ret = requests.delete(f"https://api.github.com{path}", headers=headers, data=json.dumps(args))
    if not ret.ok:
        raise Exception(f"Error: {ret.status_code} {ret.text}")
    if ret.headers.get("Content-Type","").startswith("application/json"):
        return ret.json(), ret.status_code
    else:
        return ret.text, ret.status_code
    
def put_wrapper(path: str, args: dict=None):
    token = get_secrets()
    headers = {"Authorization": "token {}".format(token)}
    ret = requests.put(f"https://api.github.com{path}", headers=headers, data=json.dumps(args))
    if not ret.ok:
        raise Exception(f"Error: {ret.status_code} {ret.text}")
    if ret.headers.get("Content-Type","").startswith("application/json"):
        return ret.json(), ret.status_code
    else:
        return ret.text, ret.status_code