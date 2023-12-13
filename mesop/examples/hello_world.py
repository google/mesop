import mesop as me


@me.page(path="/hello_world")
def hi():
  me.text(text="Hello world!")
