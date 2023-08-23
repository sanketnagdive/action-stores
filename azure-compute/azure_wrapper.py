import logging
import requests
from .secrets import get_secrets
from requests import Session

logger = logging.getLogger(__name__)


def get_api_token():
    AZURE_CLIENT_SECRET, AZURE_CLIENT_ID, AZURE_TENANT_ID = get_secrets()


    token_url = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/oauth2/v2.0/token"
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': AZURE_CLIENT_ID,
        'client_secret': AZURE_CLIENT_SECRET,
        'scope': 'https://management.azure.com/.default'
    }
    response = requests.post(token_url, data=token_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    response.raise_for_status()
    token = response.json().get('access_token')
    logger.debug(f"Token: {token}")
    return toke

def get_session():
    session = Session()
    session.headers.update({"Authorization": f"Bearer {get_api_token()}"})
    return session

def get_wrapper(endpoint: str, subscriptionId: str, api_version: str) -> dict:
    session = get_session()
    base_url = "https://management.azure.com"
    url = f"{base_url}{endpoint}?api-version={api_version}"
    response = session.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def post_wrapper(endpoint: str, subscriptionId: str, api_version: str, data: dict = None) -> dict:
    session = get_session()
    base_url = "https://management.azure.com"
    url = f"{base_url}{endpoint}?api-version={api_version}"
    response = session.post(url, json=data)
    if response.status_code == 200 or response.status_code == 201:
        return response.json()
    else:
        response.raise_for_status()

def put_wrapper(endpoint: str, subscriptionId: str, api_version: str, data: dict = None) -> dict:
    session = get_session()
    base_url = "https://management.azure.com"
    url = f"{base_url}{endpoint}?api-version={api_version}"
    response = session.put(url, json=data)
    if response.status_code == 200 or response.status_code == 201:
        logger.info(f"Successful PUT request: {url}")
        return response.json()
    else:
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logger.error(f"PUT request failed with status {response.status_code} for URL: {url}")
            logger.error(f"Error response: {response.text}")
            return {"error": str(err)}  # Return the error as a string