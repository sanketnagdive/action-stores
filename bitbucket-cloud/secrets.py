from . import action_store

def get_bitbucket_username():
    token = action_store.secrets.get("BITBUCKET_USERNAME")
    if token is None:
        raise EnvironmentError("BITBUCKET_USERNAME is not set in environment variables.")
    return token

def get_bitbcuket_app_password():
    org = action_store.secrets.get("BITBUCKET_APP_PASSWORD")
    if org is None:
        raise EnvironmentError("BITBUCKET_APP_PASSWORD is not set in environment variables.")
    return org