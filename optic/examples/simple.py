from dataclasses import dataclass
import optic as op


@dataclass
class State:
    str: str
    count: int


store = op.store(
    State(str="init", count=0),
)


@op.on(op.CheckboxEvent)
def checkbox_update(state: State, action: op.CheckboxEvent) -> State:
    if action.checked:
        state.str = "checked"
    else:
        state.str = "unchecked"
    return state


@op.on(op.ClickEvent)
def button_click(state: State, action: op.ClickEvent) -> State:
    state.count += 1
    return state


def main():
    state = store.get_state()
    op.button(label="click me", on_click=button_click)
    op.text(text=f"{state.count} clicks")
    op.checkbox(label="check?", on_update=checkbox_update)
    op.text(text=state.str)
