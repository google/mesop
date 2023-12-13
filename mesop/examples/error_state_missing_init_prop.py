import mesop as me


@me.stateclass
class State:
    valid_field: str = ""
    invalid_field: str


@me.page(path="/error_state_missing_init_prop")
def m():
    state = me.state(State)
    me.text(text="Should not succeed")
