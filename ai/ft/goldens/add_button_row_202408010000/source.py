import mesop as me


@me.stateclass
class State:
    pass


@me.page()
def hello_world():
    me.text("Hello, World!", type="headline-1")
