from dataclasses import dataclass
import optic as op


@dataclass
class State:
    str: str
    count: int


def handle_checked(state: State, action: op.Action) -> State:
    if action.payload.bool:
        state.str = "checked"
    else:
        state.str = "unchecked"
    return state


def handle_clicked(state: State, action: op.Action) -> State:
    state.count += 1
    return state


reducers = {
    "CHECKED": handle_checked,
    "CLICKED": handle_clicked,
}


def main():
    store = op.store(
        reducers,
        State(str="init", count=0),
    )

    state = store.get_state()
    op.button(label="click me", on_click="CLICKED")
    op.text(text=f"{state.count} clicks")
    op.checkbox(label="check?", on_update="CHECKED")
    op.text(text=state.str)
