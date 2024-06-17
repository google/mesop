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
    with me.box():
      me.text(
        "You can use built-in components inside the slot of a web component."
      )
      #
      me.checkbox(
        # Need to set |checked| because of https://github.com/google/mesop/issues/449
        checked=me.state(State).checked,
        label="Checked?",
        on_change=on_checked,
      )
      counter_component(
        value=me.state(State).value,
        on_decrement=on_decrement,
      )
  me.text(f"Checked? {me.state(State).checked}")


def on_checked(e: me.CheckboxChangeEvent):
  me.state(State).checked = e.checked


@me.stateclass
class State:
  checked: bool
  value: int = 10


class ChangeValue(BaseModel):
  value: int


def on_increment(e: mel.WebEvent):
  increment = ChangeValue(**e.value)
  me.state(State).value = increment.value


def on_decrement(e: mel.WebEvent):
  decrement = ChangeValue(**e.value)
  me.state(State).value = decrement.value
