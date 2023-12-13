import mesop as me


@me.stateclass
class State:
  string: str = "initial_text_state"


@me.on(me.ChangeEvent)
def change(action: me.ChangeEvent):
  state = me.state(State)
  state.string = action.value


@me.page(path="/components/text_input/e2e/text_input_app")
def app():
  me.text_input(label="simple-text-input", on_change=change)
  state = me.state(State)
  me.text(text="Text output:" + state.string)
