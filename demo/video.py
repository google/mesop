import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/video",
)
def app():
  me.video(
    src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.webm",
    style=me.Style(height=300, width=300),
  )
