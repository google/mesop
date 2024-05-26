import mesop as me


@me.stateclass
class State:
  initial_value: float = 50.0
  value: float = 50.0


def on_value_change(event: me.SliderValueChangeEvent):
  me.state(State).value = event.value


def on_input(event: me.InputEvent):
  state = me.state(State)
  state.initial_value = float(event.value)
  state.value = state.initial_value


@me.page(path="/components/slider/e2e/slider_app")
def app():
  state = me.state(State)
  me.input(label="Slider value", on_input=on_input)
  me.slider(
    on_value_change=on_value_change,
    value=state.initial_value,
    style=me.Style(width="100%"),
  )
  me.text(text=f"Value: {me.state(State).value}")
