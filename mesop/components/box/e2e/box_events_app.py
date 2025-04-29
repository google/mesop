import mesop as me


@me.stateclass
class State:
  is_click: bool = False
  is_right_click: int = False
  client_x: int = 0
  client_y: int = 0
  page_x: int = 0
  page_y: int = 0
  offset_x: int = 0
  offset_y: int = 0


@me.page(path="/components/box/e2e/box_events_app")
def app():
  state = me.state(State)
  with me.box(
    style=me.Style(width="100%", height="100%", margin=me.Margin.all(20)),
    on_click=on_click,
    on_right_click=on_right_click,
  ):
    me.text("Is Click: " + str(state.is_click))
    me.text("Is Right Click: " + str(state.is_right_click))
    me.text("Client X: " + str(state.client_x))
    me.text("Client Y: " + str(state.client_y))
    me.text("Page X: " + str(state.page_x))
    me.text("Page Y: " + str(state.page_y))
    me.text("Offset X: " + str(state.offset_x))
    me.text("Offset Y: " + str(state.offset_y))


def on_click(e: me.ClickEvent):
  state = me.state(State)
  state.is_click = True
  state.is_right_click = False
  state.client_x = int(e.client_x)
  state.client_y = int(e.client_y)
  state.page_x = int(e.page_x)
  state.page_y = int(e.page_y)
  state.offset_x = int(e.offset_x)
  state.offset_y = int(e.offset_y)


def on_right_click(e: me.ClickEvent):
  state = me.state(State)
  state.is_click = True
  state.is_right_click = True
  state.client_x = int(e.client_x)
  state.client_y = int(e.client_y)
  state.page_x = int(e.page_x)
  state.page_y = int(e.page_y)
  state.offset_x = int(e.offset_x)
  state.offset_y = int(e.offset_y)
