import mesop as me


@me.stateclass
class State:
  box_clicked: bool
  button_clicked: bool


@me.page(path="/testing/click_is_target")
def page():
  state = me.state(State)
  with me.box(on_click=on_click_box, style=me.Style(background="red")):
    me.button("Click", on_click=on_click_button, type="flat")
  me.text(f"Box clicked: {state.box_clicked}")
  me.text(f"Button clicked: {state.button_clicked}")


def on_click_box(e: me.ClickEvent):
  if e.is_target:
    me.state(State).box_clicked = True


def on_click_button(e: me.ClickEvent):
  me.state(State).button_clicked = True
