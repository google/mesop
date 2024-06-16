from pydantic import BaseModel

import mesop as me
import mesop.labs as mel
from mesop.examples.web_component.slot.counter_component import (
  counter_component,
)
from mesop.examples.web_component.slot.outer_component import (
  outer_component,
)


@me.page(
  path="/web_component/slot/slot_app",
)
def page():
  with outer_component(
    value=me.state(State).value,
    on_increment=on_increment,
  ):
    counter_component(
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
