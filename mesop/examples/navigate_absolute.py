import mesop as me


@me.page(path="/navigate_absolute")
def page1():
  me.text("Navigate to absolute URLs")
  me.button("navigate https", on_click=navigate_https)
  me.button("navigate http", on_click=navigate_http)
  me.button("navigate yield", on_click=navigate_yield)


def navigate_https(e: me.ClickEvent):
  me.navigate("https://google.com/")


def navigate_http(e: me.ClickEvent):
  me.navigate("http://example.com/")


def navigate_yield(e: me.ClickEvent):
  yield
  me.navigate("https://google.com/")
  yield
