import mesop as me


@me.stateclass
class State:
  first: bool
  second: bool


def outer_on_change(event: me.CheckboxChangeEvent):
  state = me.state(State)
  state.first = event.checked


@me.page(path="/testing/conditional_event_handler")
def app():
  def inner_on_change(event: me.CheckboxChangeEvent):
    state = me.state(State)
    state.second = event.checked

  me.text("Make sure tracing discovers event handlers that are conditional")
  me.checkbox("first checkbox", on_change=outer_on_change)
  state = me.state(State)
  if state.first:
    me.checkbox("second checkbox", on_change=inner_on_change)
  if state.second:
    me.text("second checkbox has been checked")
