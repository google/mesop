import time

import mesop as me


@me.page(path="/concurrent_updates")
def page():
  me.text("concurrent_updates")
  me.button(label="Slow state update", on_click=slow_state_update)
  me.button(label="Fast state update", on_click=fast_state_update)
  me.text("Slow state: " + str(me.state(State).slow_state))
  me.text("Fast state: " + str(me.state(State).fast_state))


@me.stateclass
class State:
  slow_state: int = 0
  fast_state: int = 0


def slow_state_update(e: me.ClickEvent):
  me.state(State).slow_state += 1
  yield
  time.sleep(3)
  me.state(State).slow_state += 1
  yield


def fast_state_update(e: me.ClickEvent):
  me.state(State).fast_state += 1
