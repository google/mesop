from pydantic import BaseModel

import mesop as me
import mesop.labs as mel
from mesop.examples.custom_component.inner_component import inner_component
from mesop.examples.custom_component.outer_component import (
  outer_component,
)


@me.page(
  path="/simple_slot_app",
)
def page():
  with outer_component(
    value=me.state(State).value,
    on_increment=on_increment,
  ):
    inner_component(
      value=me.state(State).value,
      on_decrement=on_decrement,
    )


@me.stateclass
class State:
  value: int = 10


class ChangeValue(BaseModel):
  value: int


def on_increment(e: mel.WebEvent):
  increment = ChangeValue(**e.value)
  me.state(State).value = increment.value


def on_decrement(e: mel.WebEvent):
  decrement = ChangeValue(**e.value)
  me.state(State).value = decrement.value
