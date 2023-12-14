import mesop as me


@me.stateclass
class State:
  checked: bool = True


@me.on(me.CheckboxEvent)
def on_update(event: me.CheckboxEvent):
  state = me.state(State)
  state.checked = event.checked


@me.page(path="/components/checkbox/e2e/checkbox_app")
def app():
  state = me.state(State)
  me.checkbox(
    label="checkbox", on_mat_checkbox_change=on_update, value=state.checked
  )
  if state.checked:
    me.text(text="is checked")
  else:
    me.text(text="is not checked")
