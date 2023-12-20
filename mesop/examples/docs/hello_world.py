import mesop as me


@me.page(path="/hello_world")
def app():
  me.text("Hello World")
