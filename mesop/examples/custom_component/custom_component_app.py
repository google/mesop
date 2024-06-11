import mesop as me

from .custom_component import CustomEvent, foo_custom_component


@me.page(path="/custom_component")
def page():
  me.text("custom_component12")
  foo_custom_component(value=me.state(State).value, on_event=on_foo_event)


@me.stateclass
class State:
  value: int = 3


def on_foo_event(e: CustomEvent):
  me.state(State).value = e.value
