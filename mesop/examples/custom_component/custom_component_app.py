from pydantic import BaseModel

import mesop as me
import mesop.labs as mel

from .custom_component import foo_custom_component


@me.page(
  path="/custom_component",
  security_policy=me.SecurityPolicy(
    dangerously_disable_trusted_types=True,
  ),
)
def page():
  me.text("custom_component12")
  foo_custom_component(value=me.state(State).value, on_increment=on_increment)


@me.stateclass
class State:
  value: int = 3


class Increment(BaseModel):
  value: int


def on_increment(e: mel.CustomEvent):
  increment = Increment(**e.value)
  me.state(State).value = increment.value
