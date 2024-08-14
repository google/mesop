import mesop as me


@me.page(path="/examples/boilerplate_free_event_handlers")
def page():
  state = me.state(State)
  me.text("Boilerplate-free event handlers")
  me.input(label="Name", key="name", on_blur=update_state)
  me.input(label="Address", key="address", on_blur=update_state)
  me.text(f"Name: {state.name}")
  me.text(f"Address: {state.address}")


@me.stateclass
class State:
  name: str
  address: str


def update_state(event: me.InputBlurEvent):
  state = me.state(State)
  setattr(state, event.key, event.value)
