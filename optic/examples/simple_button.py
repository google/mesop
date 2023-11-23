import optic as op


@op.stateclass
class State:
    count_clicks: int = 0


@op.on(op.ClickEvent)
def button_click(action: op.ClickEvent):
    state = op.state(State)
    state.count_clicks += 1


@op.page(path="/simple_button")
def main():
    state = op.state(State)
    op.button(label="click me", on_click=button_click)
    op.text(text=f"{state.count_clicks} clicks")
