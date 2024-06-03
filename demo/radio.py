import mesop as me


@me.stateclass
class State:
  radio_value: str = "2"


def on_change(event: me.RadioChangeEvent):
  s = me.state(State)
  s.radio_value = event.value


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/radio",
)
def app():
  s = me.state(State)
  me.text("Horizontal radio options")
  me.radio(
    on_change=on_change,
    options=[
      me.RadioOption(label="Option 1", value="1"),
      me.RadioOption(label="Option 2", value="2"),
    ],
    value=s.radio_value,
  )
  me.text(text="Selected radio value: " + s.radio_value)
