import base64
import json
import secrets
import urllib.parse as urlparse
from typing import Any, Generator, Iterable
from urllib import request as urllib_request

from flask import Response, abort, request

import mesop.protos.ui_pb2 as pb
from mesop.env.env import EXPERIMENTAL_EDITOR_TOOLBAR_ENABLED
from mesop.runtime import runtime
from mesop.server.config import app_config

LOCALHOSTS = (
  # For IPv4 localhost
  "127.0.0.1",
  # For IPv6 localhost
  "::1",
)

STREAM_END = "data: <stream_end>\n\n"


def check_editor_access():
  if not EXPERIMENTAL_EDITOR_TOOLBAR_ENABLED:
    abort(403)  # Throws a Forbidden Error
  # Prevent accidental usages of editor mode outside of
  # one's local computer
  if request.remote_addr not in LOCALHOSTS:
    abort(403)  # Throws a Forbidden Error
  # Visual editor should only be enabled in debug mode.
  if not runtime().debug_mode:
    abort(403)  # Throws a Forbidden Error


def serialize(response: pb.UiResponse) -> str:
  encoded = base64.b64encode(response.SerializeToString()).decode("utf-8")
  return f"data: {encoded}\n\n"


def generate_state_token():
  """Generates a state token used to cache and look up Mesop state."""
  return secrets.token_urlsafe(16)


def create_update_state_event(diff: bool = False) -> str:
  """Creates a state event to send to the client.

  Args:
    diff: If true, sends diffs instead of the full state objects

  Returns:
    serialized `pb.UiResponse`
  """

  state_token = ""

  # If enabled, we will save the user's state on the server, so that the client does not
  # need to send the full state back on the next user event request.
  if app_config.state_session_enabled:
    state_token = generate_state_token()
    runtime().context().save_state_to_session(state_token)

  update_state_event = pb.UpdateStateEvent(
    state_token=state_token,
    diff_states=runtime().context().diff_state() if diff else None,
    full_states=runtime().context().serialize_state() if not diff else None,
  )

  return serialize(pb.UiResponse(update_state_event=update_state_event))


def is_same_site(url1: str | None, url2: str | None):
  """
  Determine if two URLs are the same site.
  """
  # If either URL is false-y, they are not the same site
  # (because we need a real URL to have an actual site)
  if not url1 or not url2:
    return False
  try:
    p1, p2 = urlparse.urlparse(url1), urlparse.urlparse(url2)
    return p1.hostname == p2.hostname
  except ValueError:
    return False


SSE_DATA_PREFIX = "data: "


def sse_request(
  url: str, data: dict[str, Any]
) -> Generator[dict[str, Any], None, None]:
  """
  Make an SSE request and yield JSON parsed events.
  """
  headers = {
    "Content-Type": "application/json",
    "Accept": "text/event-stream",
  }
  encoded_data = json.dumps(data).encode("utf-8")
  req = urllib_request.Request(
    url, data=encoded_data, headers=headers, method="POST"
  )

  with urllib_request.urlopen(req) as response:
    for line in response:
      if line.strip():
        decoded_line = line.decode("utf-8").strip()
        if decoded_line.startswith(SSE_DATA_PREFIX):
          event_data = json.loads(decoded_line[len(SSE_DATA_PREFIX) :])
          yield event_data


def make_sse_response(
  response: Iterable[bytes] | bytes | Iterable[str] | str | None = None,
):
  return Response(
    response,
    content_type="text/event-stream",
    # "X-Accel-Buffering" impacts SSE responses due to response buffering (i.e.
    # individual events may get batched together instead of being sent right away).
    # See https://nginx.org/en/docs/http/ngx_http_proxy_module.html
    headers={"X-Accel-Buffering": "no"},
  )
