import mesop as me


@me.stateclass
class State:
  value: str


def on_load(e: me.LoadEvent):
  me.state(State).value = "on_load ran"


@me.page(path="/navigation_on_load/page1", on_load=on_load)
def page1():
  me.text("page1")
  me.text(me.state(State).value)
  me.button("navigate", on_click=navigate)


@me.page(path="/navigation_on_load/page2")
def page2():
  me.text("page2")


def navigate(e: me.ClickEvent):
  me.navigate("/navigation_on_load/page2")
