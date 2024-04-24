import mesop as me


@me.page(path="/tooltip")
def app():
  with me.tooltip(message="Tooltip message"):
    me.text(text="Hello, World")
