import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/badge",
)
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
