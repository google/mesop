import optic as op

def reducer(state: str, action: op.Action[str]) -> str:
    if action.type == 'CHECKED':
        return "checked"
    elif action.type == 'UNCHECKED':
        return "unchecked"
    return state

def main():
    store = op.store(reducer, "init")
    op.checkbox(label="check?", on_checked="CHECKED")
    op.text(text=store.get_state())
