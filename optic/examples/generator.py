from time import sleep

import optic as op


def generate_str():
  yield "foo"
  sleep(1)
  yield "bar"


@op.stateclass
class State:
  string: str = ""


@op.on(op.ClickEvent)
def button_click(action: op.ClickEvent):
  state = op.state(State)
  for val in generate_str():
    state.string += val
    yield


@op.page(path="/generator")
def main():
  state = op.state(State)
  op.button(label="click", on_click=button_click)
  op.text(text=f"{state.string}")
