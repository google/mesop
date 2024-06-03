import mesop as me


@me.stateclass
class State:
  checked: bool


def on_update(event: me.CheckboxChangeEvent):
  state = me.state(State)
  state.checked = event.checked


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/checkbox",
)
def app():
  state = me.state(State)
  me.checkbox(
    "Simple checkbox",
    on_change=on_update,
  )

  if state.checked:
    me.text(text="is checked")
  else:
    me.text(text="is not checked")
