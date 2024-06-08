import time

import mesop as me


def fake_api():
  yield 1
  time.sleep(1)
  yield 2
  time.sleep(2)
  yield 3


def on_load(e: me.LoadEvent):
  for val in fake_api():
    me.state(State).default_values.append(val)
    yield


@me.page(path="/docs/on_load", on_load=on_load)
def app():
  me.text("onload")
  me.text(str(me.state(State).default_values))


@me.stateclass
class State:
  default_values: list[int]
