import mesop as me


@me.stateclass
class State:
    pass


@me.page()
def main_page():
    me.text("Hello, World!")
