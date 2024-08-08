from pydantic import BaseModel

import mesop as me
import mesop.labs as mel
from mesop.examples.web_component.slot.counter_component import (
  counter_component,
)
from mesop.examples.web_component.slot.outer_component import (
  outer_component,
)


def on_add_checkbox_slot(e: me.ClickEvent):
  me.state(State).checkbox_slot = True


@me.page(
  path="/web_component/slot/slot_app",
  security_policy=me.SecurityPolicy(
    allowed_script_srcs=[
      "https://cdn.jsdelivr.net",
    ]
  ),
)
def page():
  s = me.state(State)
  me.button("add checkbox slot", on_click=on_add_checkbox_slot)
  with outer_component(
    value=me.state(State).value,
    on_increment=on_increment,
  ):
    with me.box():
      me.text(
        "You can use built-in components inside the slot of a web component."
      )
      if s.checkbox_slot:
        me.checkbox(
          label="Checked?",
          on_change=on_checked,
        )
      me.input(key="input", label="input slot", on_input=on_input)
      counter_component(
        key="counter",
        value=me.state(State).value,
        on_decrement=on_decrement,
      )
  me.text(f"Checked? {me.state(State).checked}")


def on_input(e: me.InputEvent):
  me.state(State).input = e.value


def on_checked(e: me.CheckboxChangeEvent):
  me.state(State).checked = e.checked


@me.stateclass
class State:
  checkbox_slot: bool = False
  input: str
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
