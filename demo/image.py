import mesop as me


def load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  on_load=load,
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/image",
)
def app():
  with me.box(style=me.Style(margin=me.Margin.all(15))):
    me.image(
      src="https://interactive-examples.mdn.mozilla.net/media/cc0-images/grapefruit-slice-332-332.jpg",
      alt="Grapefruit",
      style=me.Style(width="100%"),
    )
