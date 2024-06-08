import time

import mesop as me


def on_load(e: me.LoadEvent):
  state = me.state(State)
  state.default_values.append("a")
  yield
  time.sleep(1)
  state.default_values.append("b")
  yield


@me.page(path="/docs/on_load_generator", on_load=on_load)
def app():
  me.text("onload")
  me.text(str(me.state(State).default_values))


@me.stateclass
class State:
  default_values: list[str]
