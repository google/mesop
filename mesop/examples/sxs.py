import mesop as me


@me.page(path="/sxs")
def app():
  with me.box(style=me.Style(display="flex")):
    me.text("Hello")
    me.text("Hello")
