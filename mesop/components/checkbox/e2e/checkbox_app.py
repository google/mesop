import mesop as me


@me.stateclass
class State:
  checked: bool = True


@me.on(me.CheckboxChangeEvent)
def on_update(event: me.CheckboxChangeEvent):
  state = me.state(State)
  state.checked = event.checked


@me.page(path="/components/checkbox/e2e/checkbox_app")
def app():
  state = me.state(State)
  with me.checkbox(aria_label="checkbox", on_change=on_update):
    me.text(text="labelewe")

  if state.checked:
    me.text(text="is checked")
  else:
    me.text(text="is not checked")
