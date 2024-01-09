import mesop as me


@me.page(path="/components/badge/e2e/badge_app")
def app():
  with me.box(
    style=me.Style(
      display="block",
      padding=me.Padding(top=16, right=16, bottom=16, left=16),
      height=50,
      width=30,
      background="pink",
    )
  ):
    with me.badge(content="1"):
      me.text(text="some badge")
