from typing import Any, Callable

import mesop.labs as mel

_HOST = "generativelanguage.googleapis.com"

_GEMINI_BIDI_WEBSOCKET_URI = "wss://{host}/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent?key={api_key}"


@mel.web_component(path="./gemini_live.js")
def gemini_live(
  *,
  api_key: str = "",
  api_config: str = "",
  enabled: bool = False,
  input_prompt: str = "",
  on_start: Callable[[mel.WebEvent], Any] | None = None,
  on_stop: Callable[[mel.WebEvent], Any] | None = None,
  on_tool_call: Callable[[mel.WebEvent], Any] | None = None,
  tool_call_responses: str = "",
):
  """Sets up direct web socket connection to Gemini Live API on the client.

  This approach is not secure since it exposes the Gemini API key. It should only be
  used for demo purposes. By making the connection on the client, we reduce the burden
  on the Mesop server and lets the Mesop server focus on rendering the UI. In a more
  realistic scenario, you'd want to connect to a proxy web socket endpoint.

  It is possible to run the web socket connection the Gemini Live API on the Mesop
  server (i.e. use Mesop as the web socket proxy), but that is not scalable and a bit
  hacky. It also requires `MESOP_WEBSOCKETS_ENABLED=true`.

  Args:
    api_key: Gemini API Key
    api_config: JSON string of the Gemini Live API configuration
    enabled: Whether the Gemini Live API connection has been enabled
    input_prompt: Send a text prompt
    on_start: Event for when the Gemini Live API has been started
    on_stop: Event for when the Gemini Live API has been stopped
    on_tool_call: Event for custom tool calls made by Gemini.
    tool_call_responses: JSON string of custom tool call responses to send back to
                         Gemini Live API.
  """
  return mel.insert_web_component(
    name="gemini-live",
    events={
      "startEvent": on_start,
      "stopEvent": on_stop,
      "toolCallEvent": on_tool_call,
    },
    properties={
      "api_config": api_config,
      "enabled": enabled,
      "endpoint": _GEMINI_BIDI_WEBSOCKET_URI.format(
        host=_HOST, api_key=api_key
      ),
      "input_prompt": input_prompt,
      "tool_call_responses": tool_call_responses,
    },
  )
