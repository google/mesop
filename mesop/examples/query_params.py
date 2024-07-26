import mesop as me


@me.stateclass(query_params=True)
class State:
  a: str
  b: str
  val: int


@me.page(path="/examples/query_params")
def page():
  me.text("query_param")
  me.text("val: " + str(me.state(State).val))
  me.button("increment", on_click=increment)


def increment(e: me.ClickEvent):
  me.state(State).val += 1
