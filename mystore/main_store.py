
import sys
from pathlib import Path
from pydantic import BaseModel
import kubiya

action_store = kubiya.ActionStore("mystore", "0")

@action_store.kubiya_action(validate_input=True)
def simple_action(a: str):
    "returns bar"
    return f"hi {a} from simple_action"


class User(BaseModel):
    """used for type hints, automatic decumentation and validation"""
    name: str
    age: int

@action_store.kubiya_action(validate_input=True)
def action_with_model(user: User):
    """returns baz"""
    return f"{user.name} | {user.age}"

