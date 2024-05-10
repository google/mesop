import mesop as me


@me.stateclass
class State:
  input: str = ""


def on_input(e: me.InputEvent):
  state = me.state(State)
  state.input = e.value


@me.page(path="/textarea")
def app():
  s = me.state(State)
  me.textarea(label="Basic input", on_input=on_input)
  me.text(text=s.input)
