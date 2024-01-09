import mesop as me


@me.stateclass
class State:
  val: int = 0


def click(event: me.ClickEvent):
  state = me.state(State)
  state.val += 1


@me.page(path="/nested")
def app():
  state = me.state(State)

  with me.box(style=me.Style(background="pink")):
    me.text(text="hi1")
    with me.box(style=me.Style(background="blue")):
      me.text(text="hi2")
      with me.button(on_click=click, key="incredibly_long_key"):
        me.text(text="a button")
      with me.box(style=me.Style(background="orange")):
        me.text(text=f"{state.val} clicks")
