import mesop as me


def load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  on_load=load,
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://mesop-dev.github.io"]
  ),
  path="/embed",
)
def app():
  src = "https://mesop-dev.github.io/mesop/"
  me.text("Embedding: " + src, style=me.Style(padding=me.Padding.all(15)))
  me.embed(
    src=src,
    style=me.Style(width="100%", height="100%"),
  )
