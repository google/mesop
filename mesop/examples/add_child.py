import mesop as me


@me.page(path="/add_child")
def page():
  me.text("Hello")
  me.button("Add child", on_click=add_child)
  for i in range(me.state(State).children):
    me.text("child" + str(i))


@me.stateclass
class State:
  children: int


def add_child(e: me.ClickEvent):
  me.state(State).children += 1
