from pydantic import BaseModel

import mesop as me
import mesop.labs as mel
from mesop.examples.custom_component.custom_component import (
  foo_custom_component,
)
from mesop.examples.custom_component.inner_component import inner_component


@me.page(
  path="/custom_component",
  security_policy=me.SecurityPolicy(
    dangerously_disable_trusted_types=True,
  ),
)
def page():
  inner_component(
    value=me.state(State).value,
    on_decrement=on_decrement,
  )
  me.text("custom_component")
  with foo_custom_component(
    value=me.state(State).value,
    on_increment=on_increment,
    disabled=True,
  ):
    composite_counter()
    # inner_component(
    #   value=me.state(State).value,
    #   on_decrement=on_decrement,
    # )


def composite_counter():
  me.text("Composite Value: " + str(me.state(State).value))
  me.text("ho")
  me.button("double", on_click=double)


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


def double(e: me.ClickEvent):
  me.state(State).value *= 2
