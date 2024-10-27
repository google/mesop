import mesop as me
from mesop.examples.web_component.dynamic_slot.outer_component import (
  outer_component,
  outer_component2,
)


@me.page(
  path="/web_component/dynamic_slot/dynamic_slot_app",
  security_policy=me.SecurityPolicy(
    allowed_script_srcs=[
      "https://cdn.jsdelivr.net",
    ]
  ),
)
def page():
  s = me.state(State)
  me.checkbox("check", on_change=on_change)
  if s.checked:
    with outer_component():
      me.text("abc")
      me.text("2")
  else:
    with outer_component():
      me.text("def")
      me.text("1")
      me.text("3")
      with outer_component2():
        me.text("end")


def on_change(e: me.CheckboxChangeEvent):
  me.state(State).checked = not me.state(State).checked


@me.stateclass
class State:
  checked: bool = False
