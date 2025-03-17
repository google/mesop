import mesop as me


def load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  on_load=load,
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://mesop-dev.github.io"]
  ),
  path="/tooltip",
)
def app():
  with me.box(style=me.Style(margin=me.Margin.all(15))):
    with me.tooltip(message="Tooltip message"):
      me.text(text="Hello, World")
