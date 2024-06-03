import mesop as me


@me.stateclass
class State:
  toggled: bool = False


def on_change(event: me.SlideToggleChangeEvent):
  s = me.state(State)
  s.toggled = not s.toggled


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/slide_toggle",
)
def app():
  me.slide_toggle(label="Slide toggle", on_change=on_change)
  s = me.state(State)
  me.text(text=f"Toggled: {s.toggled}")
