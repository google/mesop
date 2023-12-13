import mesop as me


@me.stateclass
class State:
  count_clicks: int = 0


@me.on(me.ClickEvent)
def button_click(action: me.ClickEvent):
  state = me.state(State)
  state.count_clicks += 1


@me.page(path="/simple_button")
def main():
  state = me.state(State)
  me.button(label="click me", on_click=button_click)
  me.text(text=f"{state.count_clicks} clicks")
