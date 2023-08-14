import requests
from .secrets import get_secrets
import logging

logger = logging.getLogger(__name__)

def get_wrapper(path: str):
    logger.info(f"GET {path}")
    api_url, api_token = get_secrets()
    headers = {
        "Authorization": f"Token token={api_token}",
        "Accept": "application/vnd.pagerduty+json;version=2"
    }
    ret = requests.get(f"{api_url}/{path}", headers=headers)
    if not ret.ok:
        raise Exception(f"Error: {ret.status_code} {ret.text}")
    return ret.json()

def post_wrapper(endpoint: str, args: dict = None):
    logger.info(f"POST {endpoint} {args}")
    api_url, api_token = get_secrets()
    headers = {
        "Authorization": f"Token token={api_token}",
        "Accept": "application/vnd.pagerduty+json;version=2",
        "Content-Type": "application/json",
        "From": "bot@kubiya.ai"
    }
    ret = requests.post(f"{api_url}/{endpoint}", json=args, headers=headers)
    if not ret.ok:
        raise Exception(f"Error: {ret.status_code} {ret.text}")
    return ret.json()
