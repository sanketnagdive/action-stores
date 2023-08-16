from kubiya import ActionStore

action_store = ActionStore("argo", version="0.0.3")

action_store.uses_secrets(["ARGO_USER","ARGO_SERVER","ARGO_PASS"])
