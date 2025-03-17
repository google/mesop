import mesop as me


@me.stateclass
class State:
  radio_value: str = "2"


def on_change(event: me.RadioChangeEvent):
  s = me.state(State)
  s.radio_value = event.value


def load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  on_load=load,
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://mesop-dev.github.io"]
  ),
  path="/radio",
)
def app():
  s = me.state(State)
  with me.box(style=me.Style(margin=me.Margin.all(15))):
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
