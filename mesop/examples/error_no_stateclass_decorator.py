import mesop as me

class State:
    a: str

@me.page(path="/error_no_stateclass_decorator")
def app():
    me.text("Intentionally omit stateclass decorator")
    state = me.state(State)
    me.text(state.a)
