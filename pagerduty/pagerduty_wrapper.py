import requests
from .secrets import get_secrets
import logging
import os  # Import the os module

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
    from_email = os.environ.get('PAGERDUTY_FROM_EMAIL', 'bot@kubiya.ai')  # Use the environment variable 'FROM_EMAIL' if it exists, otherwise default to 'bot@kubiya.ai'
    headers = {
        "Authorization": f"Token token={api_token}",
        "Accept": "application/vnd.pagerduty+json;version=2",
        "Content-Type": "application/json",
        "From": from_email
    }
    ret = requests.post(f"{api_url}/{endpoint}", json=args, headers=headers)
    if not ret.ok:
        raise Exception(f"Error: {ret.status_code} {ret.text}")
    return ret.json()
