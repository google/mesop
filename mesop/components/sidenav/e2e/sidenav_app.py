import mesop as me


@me.stateclass
class State:
  sidenav_open: bool


def on_click(e: me.ClickEvent):
  s = me.state(State)
  s.sidenav_open = not s.sidenav_open


SIDENAV_WIDTH = 200


@me.page(path="/components/sidenav/e2e/sidenav_app")
def app():
  state = me.state(State)
  with me.sidenav(
    opened=state.sidenav_open, style=me.Style(width=SIDENAV_WIDTH)
  ):
    me.text("Inside sidenav")

  with me.box(
    style=me.Style(
      margin=me.Margin(left=SIDENAV_WIDTH if state.sidenav_open else 0),
    ),
  ):
    with me.content_button(on_click=on_click):
      me.icon("menu")
    me.markdown("Main content")
