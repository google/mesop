import optic as op


def reducer(state: str, action: op.Action) -> str:
    if action.type == 'CHECKED':
        if action.payload.bool:
            return "checked"
        else: 
            return "unchecked"

    return state

def main():
    store = op.store(reducer, "init")
    op.checkbox(label="check?", on_update="CHECKED")
    op.text(text=store.get_state())
