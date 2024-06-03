import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/audio",
)
def app():
  me.audio(
    src="https://interactive-examples.mdn.mozilla.net/media/cc0-audio/t-rex-roar.mp3",
  )
