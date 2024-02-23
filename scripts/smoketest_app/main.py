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

  me.button(
    "Button",
    on_click=button_click,
    type="flat",
    color="primary",
  )

  me.text(text=f"{state.count_clicks} clicks")
