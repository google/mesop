import mesop as me


@me.stateclass
class State:
  value: float = 0


def on_value_change(event: me.SliderValueChangeEvent):
  me.state(State).value = event.value


@me.page(path="/components/slider/e2e/slider_app")
def app():
  me.slider(on_value_change=on_value_change)
  me.text(text=f"Value: {me.state(State).value}")
