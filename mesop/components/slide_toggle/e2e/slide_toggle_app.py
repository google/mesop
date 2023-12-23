import mesop as me


@me.stateclass
class State:
  toggled: bool = False


def on_change(event: me.SlideToggleChangeEvent):
  s = me.state(State)
  s.toggled = not s.toggled


@me.page(path="/components/slide_toggle/e2e/slide_toggle_app")
def app():
  me.slide_toggle(on_change=on_change)
  s = me.state(State)
  me.text(text=f"Toggled: {s.toggled}")
