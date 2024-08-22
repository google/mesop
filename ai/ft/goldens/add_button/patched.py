import mesop as me


@me.page(path="/simple")
def page():
  me.text("Hello, world!")
  me.button("Button")
