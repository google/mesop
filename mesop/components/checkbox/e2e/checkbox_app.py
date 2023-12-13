import mesop as me


@me.stateclass
class State:
  checked: bool = False


@me.on(me.CheckboxEvent)
def on_update(event: me.CheckboxEvent):
  state = me.state(State)
  state.checked = event.checked


@me.page(path="/components/checkbox/e2e/checkbox_app")
def app():
  me.checkbox(label="checkbox", on_update=on_update)
  state = me.state(State)
  if state.checked:
    me.text(text="is checked")
  else:
    me.text(text="is not checked")
