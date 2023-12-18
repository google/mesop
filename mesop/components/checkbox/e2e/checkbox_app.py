import mesop as me


@me.stateclass
class State:
  checked: bool = True
  indeterminate: bool = True


def on_update(event: me.CheckboxChangeEvent):
  state = me.state(State)
  state.checked = event.checked


def on_indeterminate_change(event: me.CheckboxIndeterminateChangeEvent):
  state = me.state(State)
  state.indeterminate = event.indeterminate


@me.page(path="/components/checkbox/e2e/checkbox_app")
def app():
  state = me.state(State)
  with me.checkbox(
    aria_label="aria_checkbox",
    on_change=on_update,
    checked=state.checked,
    on_indeterminate_change=on_indeterminate_change,
  ):
    me.text(text="checked=True")

  if state.checked:
    me.text(text="is checked")
  else:
    me.text(text="is not checked")
