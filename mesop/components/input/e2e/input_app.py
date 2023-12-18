import mesop as me


@me.stateclass
class State:
  input: str = ""
  count: int = 0
  checked: bool = False


def on_input(e: me.InputEvent):
  state = me.state(State)
  state.input = e.value


def on_change(e: me.CheckboxChangeEvent):
  state = me.state(State)
  state.checked = e.checked


@me.page(path="/components/input/e2e/input_app")
def app():
  me.text(text="Hello, world!")
  with me.checkbox(on_change=on_change):
    me.text(text="check")
  s = me.state(State)
  me.input(label="Basic input", on_input=on_input, key=str(s.checked))
  me.text(text=s.input)
