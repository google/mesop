import mesop as me

SIDENAV_WIDTH = 200


@me.stateclass
class State:
  sidenav_open: bool


def on_click(e: me.ClickEvent):
  s = me.state(State)
  s.sidenav_open = not s.sidenav_open


def opened_changed(e: me.SidenavOpenedChangedEvent):
  s = me.state(State)
  s.sidenav_open = e.opened


@me.page(path="/components/sidenav/e2e/sidenav_app_position")
def app():
  state = me.state(State)
  with me.sidenav(
    opened=state.sidenav_open,
    position="end",
    disable_close=False,
    on_opened_changed=opened_changed,
    style=me.Style(
      border_radius=0,
      width=SIDENAV_WIDTH,
      background=me.theme_var("surface-container-low"),
      padding=me.Padding.all(15),
    ),
  ):
    me.text("Inside sidenav")

  with me.box(
    style=me.Style(
      margin=me.Margin(left=SIDENAV_WIDTH if state.sidenav_open else 0),
      padding=me.Padding.all(15),
    ),
  ):
    with me.content_button(on_click=on_click):
      me.icon("menu")
    me.markdown("Main content")
