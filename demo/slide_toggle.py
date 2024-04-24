import mesop as me


@me.stateclass
class State:
  toggled: bool = False


def on_change(event: me.SlideToggleChangeEvent):
  s = me.state(State)
  s.toggled = not s.toggled


@me.page(path="/slide_toggle")
def app():
  me.slide_toggle(label="Slide toggle", on_change=on_change)
  s = me.state(State)
  me.text(text=f"Toggled: {s.toggled}")
