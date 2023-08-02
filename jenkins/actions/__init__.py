import time
from os import environ
from pprint import pprint
from kubiya import ActionStore, get_secret


action_store = ActionStore("jenkins", "0.1.0")
action_store.uses_secrets(["JENKINS_URL", "JENKINS_PASSWORD", "JENKINS_USER"])