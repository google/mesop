import mesop as me


@me.stateclass
class State:
  toggled: bool = False


def on_change(event: me.SlideToggleChangeEvent):
  s = me.state(State)
  s.toggled = not s.toggled


def load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  on_load=load,
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://mesop-dev.github.io"]
  ),
  path="/slide_toggle",
)
def app():
  with me.box(style=me.Style(margin=me.Margin.all(15))):
    me.slide_toggle(label="Slide toggle", on_change=on_change)
    s = me.state(State)
    me.text(text=f"Toggled: {s.toggled}")
