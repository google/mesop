import mesop as me


@me.page(path="/sxs")
def app():
  with me.box(style=me.Style(display="flex")):
    with me.box(style=me.Style(width="50%", display="inline-block")):
      me.text("Hello")
    with me.box(style=me.Style(width="50%", display="inline-block")):
      me.text("Hello")
