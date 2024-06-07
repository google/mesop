import mesop as me


def on_load(e: me.LoadEvent):
  me.state(State).default_values = ["a", "b"]


@me.page(path="/on_load", on_load=on_load)
def app():
  me.button("navigate to /on_load_generator", on_click=navigate)
  me.text("/on_load " + str(me.state(State).default_values))
  with me.box():
    me.text("make sure this diffs - 2")


def navigate(e: me.ClickEvent):
  me.navigate("/on_load_generator")


@me.stateclass
class State:
  default_values: list[str]
