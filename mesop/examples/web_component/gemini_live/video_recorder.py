from typing import Any, Callable, Literal

import mesop.labs as mel


@mel.web_component(path="./video_recorder.js")
def video_recorder(
  *,
  enabled: bool = False,
  state: Literal["disabled", "initializing", "recording"] = "disabled",
  on_data: Callable[[mel.WebEvent], Any] | None = None,
  on_state_change: Callable[[mel.WebEvent], Any] | None = None,
):
  """Records video and streams video to the Mesop server or another web component.

  This web component is designed to work with `MESOP_WEBSOCKETS_ENABLED=true` when
  streaming video to the Mesop server.

  If streaming to other web components, then the default SSE mode is fine.

  This component is highly coupled to the gemini_live component since it is hardcoded
  to listen for custom Lit events that emit from that component.

  Note that this component does not have a button to enable the video recording. It must
  be triggered by a separate event, which can be forwarded to this component. For
  example, create a button with an event handler that updates state to set
  `enabled=True`.

  It should also be noted that screenshare has not been implemented. But should be
  relatively easy to add.

  Args:
    enabled: Whether the video recorder should be recording on the webcam
    state: Current state of the webcam
    on_data: Recorded video frame (jpeg at 2fps). Sent as a base64 encoded string.
    on_state_change: Notifications when webcam state changes. Mainly used for custom
                     button styling.
  """
  return mel.insert_web_component(
    name="video-recorder",
    events={
      "dataEvent": on_data,
      "stateChangeEvent": on_state_change,
    },
    properties={
      "enabled": enabled,
      "state": state,
    },
  )
