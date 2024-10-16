import time

import mesop as me


@me.page(path="/concurrent_updates_websockets")
def page():
  state = me.state(State)
  me.text("concurrent_updates_websockets")
  me.button(label="Slow state update", on_click=slow_state_update)
  me.button(label="Fast state update", on_click=fast_state_update)
  me.text("Slow state: " + str(state.slow_state))
  me.text("Fast state: " + str(state.fast_state))
  if state.show_box:
    with me.box():
      me.text("Box!")


@me.stateclass
class State:
  show_box: bool
  slow_state: bool
  fast_state: bool


def slow_state_update(e: me.ClickEvent):
  time.sleep(3)
  me.state(State).show_box = True
  me.state(State).slow_state = True
  yield


def fast_state_update(e: me.ClickEvent):
  me.state(State).show_box = True
  me.state(State).fast_state = True
