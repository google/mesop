import mesop as me


@me.page(path="/badge")
def app():
  with me.box(
    style=me.Style(
      display="block",
      padding=me.Padding(top=16, right=16, bottom=16, left=16),
      height=50,
      width=30,
    )
  ):
    with me.badge(content="1", size="medium"):
      me.text(text="text with badge")
