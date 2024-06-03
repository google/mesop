import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/embed",
)
def app():
  src = "https://google.github.io/mesop/"
  me.text("Embedding: " + src)
  me.embed(
    src=src,
    style=me.Style(width="100%", height="100%"),
  )
