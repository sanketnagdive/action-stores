from . import action_store

def get_secrets():
    api_url = action_store.secrets.get("PAGERDUTY_API_URL")
    api_token = action_store.secrets.get("PAGERDUTY_API_TOKEN")
    return api_url, api_token
