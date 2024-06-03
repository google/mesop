import mesop as me


@me.stateclass
class State:
  initial_input_value: str = "50.0"
  initial_slider_value: float = 50.0
  slider_value: float = 50.0


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/slider",
)
def app():
  state = me.state(State)
  with me.box(style=me.Style(display="flex", flex_direction="column")):
    me.input(
      label="Slider value", value=state.initial_input_value, on_input=on_input
    )
    me.slider(on_value_change=on_value_change, value=state.initial_slider_value)
    me.text(text=f"Value: {me.state(State).slider_value}")


def on_value_change(event: me.SliderValueChangeEvent):
  state = me.state(State)
  state.slider_value = event.value
  state.initial_input_value = str(state.slider_value)


def on_input(event: me.InputEvent):
  state = me.state(State)
  state.initial_slider_value = float(event.value)
  state.slider_value = state.initial_slider_value
