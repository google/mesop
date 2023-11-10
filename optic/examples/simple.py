from dataclasses import dataclass
import optic as op

@dataclass
class State:
    str: str
    count: int

def reducer(state: State, action: op.Action) -> State:
    if action.type == 'CHECKED':
        if action.payload.bool:
            state.str = "checked"
            return state
        else: 
            state.str = "unchecked"
            return state
    if action.type == 'CLICKED':
        state.count += 1
        return state

    return state

def main():
    store = op.store(reducer, State(str="init", count=0))
    state = store.get_state()
    op.button(label="click me", on_click="CLICKED")
    op.text(text=f"{state.count} clicks")
    op.checkbox(label="check?", on_update="CHECKED")
    op.text(text=state.str)
