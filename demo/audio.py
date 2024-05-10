import mesop as me


@me.page(path="/audio")
def app():
  me.audio(
    src="https://interactive-examples.mdn.mozilla.net/media/cc0-audio/t-rex-roar.mp3",
  )
