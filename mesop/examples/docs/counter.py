import mesop as me


@me.stateclass
class State:
  clicks: int


def button_click(event: me.ClickEvent):
  state = me.state(State)
  state.clicks += 1


@me.page(path="/counter")
def main():
  state = me.state(State)
  me.text(f"Clicks: {state.clicks}")
  with me.button(on_click=button_click):
    me.text("Increment")
