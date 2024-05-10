import mesop as me


@me.page(path="/input_race")
def app():
  state = me.state(State)
  me.input(key="a", label="Input a", on_input=on_input)
  me.input(key="b", label="Input b", on_input=on_input)
  me.button(label="Click", on_click=on_click)
  me.text("State.input_a: " + state.input_a)
  me.text("State.input_b: " + state.input_b)
  me.text("State.input_on_click: " + state.input_on_click)


@me.stateclass
class State:
  input_a: str
  input_b: str
  input_on_click: str


def on_input(e: me.InputEvent):
  state = me.state(State)
  if e.key == "a":
    state.input_a = e.value
  elif e.key == "b":
    state.input_b = e.value


def on_click(e: me.ClickEvent):
  state = me.state(State)
  state.input_on_click = state.input_a
