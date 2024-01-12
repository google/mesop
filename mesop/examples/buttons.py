import mesop as me


@me.stateclass
class State:
  count_clicks: int = 0


def button_click(event: me.ClickEvent):
  state = me.state(State)
  state.count_clicks += 1


@me.page(path="/buttons")
def main():
  state = me.state(State)
  with me.button(
    on_click=button_click, type="flat", color="primary", disabled=False
  ):
    me.text(text="primary color button")

  with me.button(on_click=button_click, type="flat"):
    me.text(text="flat button")

  with me.button(on_click=button_click, type="raised"):
    me.text(text="raised button")

  with me.button(on_click=button_click, type="stroked"):
    me.text(text="stroked button")

  me.text(text=f"{state.count_clicks} clicks")
