import mesop as me


@me.stateclass
class State:
  string: str = "initial_text_state"
  hide_text_input = False


@me.on(me.ChangeEvent)
def change(action: me.ChangeEvent):
  state = me.state(State)
  state.string = action.value


@me.on(me.CheckboxChangeEvent)
def change_checkbox(event: me.CheckboxChangeEvent):
  state = me.state(State)
  state.hide_text_input = event.checked


@me.page(path="/components/text_input/e2e/text_input_app")
def app():
  state = me.state(State)
  me.checkbox(aria_label="hide_text_input", on_change=change_checkbox)
  if not state.hide_text_input:
    me.text_input(
      label="simple-text-input", default_value=state.string, on_change=change
    )
    me.text(text="Text output:" + state.string)
