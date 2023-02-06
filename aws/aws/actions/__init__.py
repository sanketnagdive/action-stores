"""instatiate action and declare it's secrets"""
import kubiya

action_store = kubiya.ActionStore(
    "aws", "0.1.6", "https://d0.awsstatic.com/logos/powered-by-aws-white.png"
)

action_store.uses_secrets(
    [
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_SESSION_TOKEN",
        "AWS_DEFAULT_REGION",
    ]
)
