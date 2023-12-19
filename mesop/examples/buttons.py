import mesop as me
from mesop.examples.shared.navmenu import scaffold


@me.stateclass
class State:
  count_clicks: int = 0


def button_click(action: me.ClickEvent):
  state = me.state(State)
  state.count_clicks += 1


@me.page(path="/buttons")
def main():
  with scaffold(url="/buttons"):
    state = me.state(State)
    with me.button(on_click=button_click):
      me.text(text="default")
    with me.button(on_click=button_click, variant="flat"):
      me.text(text="mat-flat-button")
    with me.button(on_click=button_click, variant="raised"):
      me.text(text="mat-raised-button")
    with me.button(on_click=button_click, variant="stroked"):
      me.text(text="mat-stroked-button")
    me.text(text=f"{state.count_clicks} clicks")
