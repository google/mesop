import mesop as me


def load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  on_load=load,
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://mesop-dev.github.io"]
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
