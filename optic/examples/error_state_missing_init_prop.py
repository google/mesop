import optic as op


@op.stateclass
class State:
    valid_field: str = ""
    invalid_field: str


@op.page(path="/error_state_missing_init_prop")
def m():
    state = op.state(State)
    op.text(text="Should not succeed")
