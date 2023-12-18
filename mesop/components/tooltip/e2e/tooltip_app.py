import mesop as me


@me.page(path="/components/tooltip/e2e/tooltip_app")
def app():
  with me.tooltip(message="Hello, world!"):
    me.text(text="sometext")
  with me.box(
    style="""
    display: block;
  height: 50px;
  background: pink;
  """
  ):
    pass
  with me.tooltip(message="Second tooltip!"):
    me.text(text="sometext")
