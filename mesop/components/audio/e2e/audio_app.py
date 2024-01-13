import mesop as me


@me.page(path="/components/audio/e2e/audio_app")
def app():
  me.audio(
    src="https://interactive-examples.mdn.mozilla.net/media/cc0-audio/t-rex-roar.mp3",
  )
