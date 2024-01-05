import mesop as me


@me.page(path="/components/box/e2e/box_app")
def app():
  with me.box(
    style="""
  background-color: pink;
  height: 50px
  """
  ):
    me.text(text="hi1")
    me.text(text="hi2")
