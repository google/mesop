import mesop as me


@me.page(path="/concurrency_state")
def page():
  me.text("concurrency_state")
  me.input(label="State input", on_input=on_input)
  me.text("Input: " + me.state(State).input)


@me.stateclass
class State:
  input: str


def on_input(e: me.InputEvent):
  me.state(State).input = e.value
