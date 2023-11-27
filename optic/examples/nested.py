import optic as op


@op.stateclass
class State:
    val: int = 0


@op.on(op.ClickEvent)
def click(event: op.ClickEvent):
    state = op.state(State)
    state.val += 1


@op.page(path="/nested")
def app():
    state = op.state(State)

    with op.box(background_color="pink"):
        op.text(text="hi1")
        with op.box(background_color="blue"):
            op.text(text="hi2")
            op.button(label="a button", on_click=click, key="incredibly_long_key")
            with op.box(background_color="orange"):
                op.text(text=f"{state.val} clicks")
