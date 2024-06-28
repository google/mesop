import mesop as me


@me.stateclass
class State:
  checks: dict[str, bool]


def on_user_checkbox_change(event: me.CheckboxChangeEvent):
  state = me.state(State)
  state.checks[event.key] = event.checked


@me.page(path="/dict_state")
def app():
  state = me.state(State)

  me.checkbox(
    label="box1",
    on_change=on_user_checkbox_change,
    key="box1",
  )

  me.checkbox(
    label="box2",
    on_change=on_user_checkbox_change,
    key="box2",
  )

  me.text("Checks: " + str(state.checks.items()))
