import mesop as me


@me.page(path="/examples/box")
def page():
  with me.box(
    style=me.Style(
      max_width=400,
      min_width=200,
      max_height=300,
      min_height=100,
    )
  ):
    me.text("min/max width/height")
