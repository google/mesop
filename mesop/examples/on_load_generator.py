import time

import mesop as me


def on_load(e: me.LoadEvent):
  yield
  time.sleep(3)
  state = me.state(State)
  state.appended_values = []
  state.appended_values.append("a")
  state.replaced_values = ["1", "2", "3"]
  state.default_value = "<not-default>"
  yield
  time.sleep(3)
  state.appended_values.append("b")
  state.replaced_values = ["4", "5", "6"]
  yield


@me.page(path="/on_load_generator", on_load=on_load)
def app():
  state = me.state(State)
  me.button("navigate to /on_load", on_click=navigate)
  me.text("/on_load_generator " + str(state.appended_values))
  me.divider()
  me.text("Default value")
  me.text(state.default_value)

  me.divider()
  me.text("Replaced values")
  with me.box(key="replaced values"):
    for i in state.replaced_values:
      me.text(i)


def navigate(e: me.ClickEvent):
  me.navigate("/on_load")


@me.stateclass
class State:
  appended_values: list[str]
  replaced_values: list[str]
  default_value: str = "<init>"
