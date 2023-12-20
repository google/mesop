import mesop as me


@me.stateclass
class State:
  is_toggled: bool


def on_click(e: me.ClickEvent):
  state = me.state(State)
  state.is_toggled = not state.is_toggled


@me.page(path="/components/box/e2e/box_app")
def app():
  with me.box(
    style="""
    display: block;
  background-color: pink;
  height: 50px;
  """
  ):
    me.text(text="hi1")
    me.text(text="hi2")

  with me.box(
    on_click=on_click,
    style="""
  background-color: lightblue;
  height: 50px;
  width: 50px;
  cursor: pointer;
  position: relative;
  """,
  ):
    me.text("click me")
    if me.state(State).is_toggled:
      with me.box(
        style="""
      height: 100px;
      width: 100px;
      background: orange;
      position: absolute;
      left: 48px;
      top: 48px;
      """
      ):
        me.text("in popover")
  me.text("some other text")
