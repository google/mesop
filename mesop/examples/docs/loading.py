import time

import mesop as me


def slow_blocking_api_call():
  time.sleep(2)
  return "foo"


@me.stateclass
class State:
  data: str
  is_loading: bool


def button_click(event: me.ClickEvent):
  state = me.state(State)
  state.is_loading = True
  yield
  data = slow_blocking_api_call()
  state.data = data
  state.is_loading = False
  yield


@me.page(path="/loading")
def main():
  state = me.state(State)
  if state.is_loading:
    me.progress_spinner()
  me.text(state.data)
  me.button("Call API", on_click=button_click)
