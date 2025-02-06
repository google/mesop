import base64
from typing import Any, Callable

import mesop.labs as mel


@mel.web_component(path="./audio_player.js")
def audio_player(
  *,
  enabled: bool = False,
  data: bytes = b"",
  on_play: Callable[[mel.WebEvent], Any] | None = None,
  on_stop: Callable[[mel.WebEvent], Any] | None = None,
):
  """Plays audio streamed from the server or from other web components.

  This is a barebones configuration that sets the sample rate to 24000hz since that is
  what Gemini returns. In addition we expect the data to be in PCM format.

  This component is designed to play audio from the server and also from other web
  components. In the latter case, it will listen for an event called
  `audio-output-received`.

  This component is highly coupled to the gemini_live component since it is hardcoded to
  listen for custom Lit events that emit from that component.

  Note that this component uses slots, so that you can use native Mesop components for
  the button.

  Args:
    enabled: Whether the component is enabled
    data: Base64 encoded audio chunk to play. An important thing to note is that the
          audio player does not persist the data it receives. Instead the data is stored
          in a queue and removed once the audio has been played. This is only used if
          you're sending audio data from the server.
    on_play: Event handler for when the play button is pressed. For this demo, audio
             will automatically play when the gemini_live component has been started.
    on_stop: Event handler for when the stop button is pressed. For this demo, the stop
             button has been removed.
  """
  return mel.insert_web_component(
    name="audio-player",
    events={
      "playEvent": on_play,
      "stopEvent": on_stop,
    },
    properties={
      "enabled": enabled,
      "data": base64.b64encode(data).decode("utf-8"),
    },
  )
