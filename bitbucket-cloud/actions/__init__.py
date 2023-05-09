"""instatiate action and declare it's secrets"""
import kubiya

action_store = kubiya.ActionStore(
    "bitbucket-cloud", "0.1.0", "https://seeklogo.com/images/B/bitbucket-logo-D072214725-seeklogo.com.png"
)

action_store.uses_secrets(
    [
        "BITBUCKET_USERNAME",
        "BITBUCKET_APP_PASSWORD",
    ]
)
