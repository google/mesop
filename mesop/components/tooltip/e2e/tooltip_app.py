import mesop as me


@me.page(path="/components/tooltip/e2e/tooltip_app")
def app():
  with me.tooltip(message="Hello, world!"):
    me.text(text="sometext")
