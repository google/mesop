import mesop as me


@me.page(path="/image")
def app():
  me.image(
    src="https://interactive-examples.mdn.mozilla.net/media/cc0-images/grapefruit-slice-332-332.jpg",
    alt="Grapefruit",
    style=me.Style(width="100%"),
  )
