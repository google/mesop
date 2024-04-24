import mesop as me


@me.page(path="/embed")
def app():
  src = "https://google.github.io/mesop/"
  me.text("Embedding: " + src)
  me.embed(
    src=src,
    style=me.Style(width="100%", height="100%"),
  )
