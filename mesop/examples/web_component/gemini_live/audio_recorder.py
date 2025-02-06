from typing import Any, Callable, Literal

import mesop.labs as mel


@mel.web_component(path="./audio_recorder.js")
def audio_recorder(
  *,
  state: Literal["disabled", "initializing", "recording"] = "disabled",
  on_data: Callable[[mel.WebEvent], Any] | None = None,
  on_state_change: Callable[[mel.WebEvent], Any] | None = None,
):
  """Records audio and streams audio to the Mesop server or other web components.

  This web component is designed to work with `MESOP_WEBSOCKETS_ENABLED=true` when
  streaming audio to the Mesop server.

  If streaming to other web components, then the default SSE mode is fine.

  The `on_data` event returns continuous chunk of audio in base64-encoded PCM format
  with 16000hz sampling rate. For some reason the Gemini Live API only accepts the PCM
  data 16000hz. At 48000hz, nothing is returned. Perhaps there is a setting to override
  the expected sampling rate when sent to the Gemini Live API. Unfortunately, the docs
  are very sparse right now.

  The data event looks like:

    {
      "data": <base64-encoded-string>
    }

  This component is highly coupled to the gemini_live component since it is hardcoded
  to listen for custom Lit events that emit from that component.

  Note that this component uses slots, so that you can use native Mesop components for
  the button.

  Args:
    state: Current state of the microphone
    on_data: Recorded audio chunk
    on_state_change: Notifications when microphone state changes. Mainly used for custom
                     button styling.
  """
  return mel.insert_web_component(
    name="audio-recorder",
    events={
      "dataEvent": on_data,
      "stateChangeEvent": on_state_change,
    },
    properties={
      "state": state,
    },
  )
