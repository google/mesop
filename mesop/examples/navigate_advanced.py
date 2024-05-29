import mesop as me


@me.page(path="/navigate_advanced/page1")
def page1():
  me.text("page1")
  me.button("navigate", on_click=navigate)


@me.page(path="/navigate_advanced/page2")
def page2():
  me.text("page2")


def navigate(e: me.ClickEvent):
  me.navigate("/navigate_advanced/page2")
  yield

  yield
