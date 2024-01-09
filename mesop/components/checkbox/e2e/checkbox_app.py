import mesop as me


@me.stateclass
class State:
  checked: bool = True
  indeterminate: bool = True


def on_update(event: me.CheckboxChangeEvent):
  state = me.state(State)
  state.checked = event.checked


@me.page(path="/components/checkbox/e2e/checkbox_app")
def app():
  state = me.state(State)
  with me.checkbox(
    on_change=on_update,
    checked=state.checked,
  ):
    me.text(text="label")

  if state.checked:
    me.text(text="is checked")
  else:
    me.text(text="is not checked")
