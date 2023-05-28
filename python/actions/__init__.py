import time
from os import environ
from pprint import pprint
import logging

from kubiya import ActionStore, get_secret

actionstore = ActionStore("python", "0.1.0")

logging.basicConfig(level=logging.INFO)