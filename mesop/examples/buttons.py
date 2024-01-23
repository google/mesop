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
    "primary color button",
    on_click=button_click,
    type="flat",
    color="primary",
    disabled=False,
  )

  me.button("flat button", on_click=button_click, type="flat")

  me.button("raised button", on_click=button_click, type="raised")

  me.button("stroked button", on_click=button_click, type="stroked")

  me.text(text=f"{state.count_clicks} clicks")
