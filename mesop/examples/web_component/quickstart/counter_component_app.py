from pydantic import BaseModel

import mesop as me
import mesop.labs as mel
from mesop.examples.web_component.quickstart.counter_component import (
  counter_component,
)


@me.page(
  path="/web_component/quickstart/counter_component_app",
)
def page():
  counter_component(
    value=me.state(State).value,
    on_decrement=on_decrement,
  )


@me.stateclass
class State:
  value: int = 10


class ChangeValue(BaseModel):
  value: int


def on_decrement(e: mel.WebEvent):
  # Creating a Pydantic model from the JSON value of the WebEvent
  # to enforce type safety.
  decrement = ChangeValue(**e.value)
  me.state(State).value = decrement.value
