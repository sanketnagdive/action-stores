import time
from os import environ
from pprint import pprint

from kubiya import ActionStore, get_secret

actionstore = ActionStore("aws-local", "0.1.0")
