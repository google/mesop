import mesop as me


@me.page(path="/starter_kit")
def page():
  with me.box(
    style=me.Style(
      background="#e7f2ff",
      height="100%",
      display="flex",
      flex_direction="column",
    )
  ):
    me.text("Mesop starter kit")
