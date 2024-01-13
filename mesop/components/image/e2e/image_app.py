import mesop as me


@me.page(path="/components/image/e2e/image_app")
def app():
  me.image(
    src="https://interactive-examples.mdn.mozilla.net/media/cc0-images/grapefruit-slice-332-332.jpg",
    alt="Grapefruit",
    style=me.Style(width="150px", height="150px"),
  )
