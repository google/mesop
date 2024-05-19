import base64

import mesop as me


@me.page(path="/components/mic/e2e/mic_app")
def app():
  s = me.state(State)
  me.mic(on_chunk=on_chunk)
  me.text("Transcript: " + s.transcript)
  if s.contents:
    me.audio(src=s.contents)


@me.stateclass
class State:
  transcript: str
  contents: str


def on_chunk(e: me.AudioChunkEvent):
  transcript = e.transcript
  s = me.state(State)
  s.transcript = transcript
  data = e.data
  s.contents = f"data:audio/webm;base64,{base64.b64encode(data).decode()}"
