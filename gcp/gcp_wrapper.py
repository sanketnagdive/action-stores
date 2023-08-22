import logging
from pydantic import BaseModel
from typing import Optional, List, Dict
import json

from google.oauth2 import service_account
from google.cloud import compute_v1

from . import action_store as action_store

logging.basicConfig(level=logging.INFO)

# The action store definition is declared in the __init__.py file
# This is the main file that is executed when the action store is deployed

# This is a simple action that returns a string
# It is not validated, so you can pass anything as an input

@action_store.kubiya_action(validate_input=True)
def clients_networks(input):
    json_acct_info = json.loads(action_store.secrets.get("GOOGLE_APPLICATION_CREDENTIALS"),strict=False)
    credentials = service_account.Credentials.from_service_account_info(json_acct_info)

    networks_client = compute_v1.NetworksClient(credentials=credentials)
    networks=[network.name for network in networks_client.list(project='kubiya-test-396219')]

    return networks