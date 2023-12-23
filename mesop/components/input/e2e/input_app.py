import mesop as me


@me.stateclass
class State:
  input: str = ""


def on_input(e: me.InputEvent):
  state = me.state(State)
  state.input = e.value


@me.page(path="/components/input/e2e/input_app")
def app():
  s = me.state(State)
  me.input(label="Basic input", on_input=on_input)
  me.text(text=s.input)

  me.input(label="Textarea", type=me.Textarea(), on_input=on_input)
  me.input(label="Number input", type="number", on_input=on_input)
