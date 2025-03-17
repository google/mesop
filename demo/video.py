import mesop as me


def load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  on_load=load,
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://mesop-dev.github.io"]
  ),
  path="/video",
)
def app():
  with me.box(style=me.Style(margin=me.Margin.all(15))):
    me.video(
      src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.webm",
      style=me.Style(height=300, width=300),
    )
