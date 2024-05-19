import mesop as me


@me.page(path="/components/mic/e2e/mic_app")
def app():
  me.mic(label="Hello, world!")
