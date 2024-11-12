import mesop as me


@me.stateclass
class State:
  page_1_onload_counter: int
  page_2_onload_counter: int


def page_1_on_load(e: me.LoadEvent):
  me.state(State).page_1_onload_counter += 1


@me.page(path="/browser_navigation_on_load/page1", on_load=page_1_on_load)
def page1():
  me.text("page1")
  me.text(f"onload ran {me.state(State).page_1_onload_counter} times")
  me.button("navigate", on_click=navigate)


def navigate(e: me.ClickEvent):
  me.navigate("/browser_navigation_on_load/page2")


def page_2_on_load(e: me.LoadEvent):
  me.state(State).page_2_onload_counter += 1


@me.page(path="/browser_navigation_on_load/page2", on_load=page_2_on_load)
def page2():
  me.text("page2")
  me.text(f"onload ran {me.state(State).page_2_onload_counter} times")
