import base64
import secrets
import time
import urllib.parse as urlparse
from typing import Generator, Sequence

from flask import Flask, Response, abort, request, stream_with_context

import mesop.protos.ui_pb2 as pb
from mesop.component_helpers import diff_component
from mesop.editor.component_configs import get_component_configs
from mesop.events import LoadEvent
from mesop.exceptions import format_traceback
from mesop.runtime import runtime
from mesop.server.config import app_config
from mesop.warn import warn

LOCALHOSTS = (
  # For IPv4 localhost
  "127.0.0.1",
  # For IPv6 localhost
  "::1",
)

STREAM_END = "data: <stream_end>\n\n"


def is_processing_request():
  return _requests_in_flight > 0


_requests_in_flight = 0


def configure_flask_app(
  *, prod_mode: bool = True, exceptions_to_propagate: Sequence[type] = ()
) -> Flask:
  flask_app = Flask(__name__)

  def render_loop(
    path: str,
    trace_mode: bool = False,
    init_request: bool = False,
  ) -> Generator[str, None, None]:
    try:
      runtime().run_path(path=path, trace_mode=trace_mode)
      page_config = runtime().get_page_config(path=path)
      title = page_config.title if page_config else "Unknown path"

      root_component = runtime().context().current_node()
      previous_root_component = runtime().context().previous_node()
      component_diff = None
      if not trace_mode and previous_root_component:
        component_diff = diff_component(previous_root_component, root_component)
        root_component = None
      commands = runtime().context().commands()
      # Need to clear commands so that we don't keep on re-sending commands
      # (e.g. scroll into view) for the same context (e.g. multiple render loops
      # when processing a generator handler function)
      runtime().context().clear_commands()
      data = pb.UiResponse(
        render=pb.RenderEvent(
          root_component=root_component,
          component_diff=component_diff,
          commands=commands,
          component_configs=None
          if prod_mode or not init_request
          else get_component_configs(),
          title=title,
        )
      )
      yield serialize(data)
    except Exception as e:
      print(e)
      if e in exceptions_to_propagate:
        raise e
      yield from yield_errors(
        error=pb.ServerError(exception=str(e), traceback=format_traceback())
      )

  def yield_errors(error: pb.ServerError) -> Generator[str, None, None]:
    if not runtime().debug_mode:
      error.ClearField("traceback")
      # Redact developer errors
      if "Mesop Internal Error:" in error.exception:
        error.exception = "Sorry, there was an internal error with Mesop."
      if "Mesop Developer Error:" in error.exception:
        error.exception = (
          "Sorry, there was an error. Please contact the developer."
        )

    ui_response = pb.UiResponse(error=error)

    yield serialize(ui_response)
    yield STREAM_END

  def generate_data(ui_request: pb.UiRequest) -> Generator[str, None, None]:
    try:
      # Wait for hot reload to complete on the server-side before processing the
      # request. This avoids a race condition where the client-side reloads before
      # the server has reloaded.
      runtime().wait_for_hot_reload()
      if runtime().has_loading_errors():
        # Only showing the first error since our error UI only
        # shows one error at a time, and in practice there's usually
        # one error.
        yield from yield_errors(runtime().get_loading_errors()[0])

      if ui_request.HasField("init"):
        runtime().context().set_theme_settings(ui_request.init.theme_settings)
        runtime().context().set_viewport_size(ui_request.init.viewport_size)
        page_config = runtime().get_page_config(path=ui_request.path)
        if page_config and page_config.on_load:
          result = page_config.on_load(
            LoadEvent(
              path=ui_request.path,
            )
          )
          # on_load is a generator function then we need to iterate through
          # the generator object.
          if result:
            for _ in result:
              yield from render_loop(path=ui_request.path, init_request=True)
              runtime().context().set_previous_node_from_current_node()
              runtime().context().reset_current_node()
          else:
            yield from render_loop(path=ui_request.path, init_request=True)
        else:
          yield from render_loop(path=ui_request.path, init_request=True)
        yield create_update_state_event()
        yield STREAM_END
      elif ui_request.HasField("user_event"):
        event = ui_request.user_event
        runtime().context().set_theme_settings(event.theme_settings)
        runtime().context().set_viewport_size(event.viewport_size)

        if event.states.states:
          runtime().context().update_state(event.states)
        else:
          runtime().context().restore_state_from_session(event.state_token)

        for _ in render_loop(path=ui_request.path, trace_mode=True):
          pass
        if ui_request.user_event.handler_id:
          runtime().context().set_previous_node_from_current_node()
        else:
          # Set previous node to None to skip component diffs on hot reload. This is
          # because we lose the previous state before hot reloading, which results in
          # no diff.
          #
          # This will also skip component diffs for back button events on the browser
          # since no event handler ID is provided in that case.
          runtime().context().reset_previous_node()
        runtime().context().reset_current_node()

        result = runtime().context().run_event_handler(ui_request.user_event)
        path = ui_request.path
        has_run_navigate_on_load = False
        for _ in result:
          navigate_commands = [
            command
            for command in runtime().context().commands()
            if command.HasField("navigate")
          ]
          if len(navigate_commands) > 1:
            warn(
              "Dedicated multiple navigate commands! Only the first one will be used."
            )
          for command in runtime().context().commands():
            if command.HasField("navigate"):
              path = command.navigate.url
              page_config = runtime().get_page_config(path=path)
              if (
                page_config
                and page_config.on_load
                and not has_run_navigate_on_load
              ):
                has_run_navigate_on_load = True
                result = page_config.on_load(LoadEvent(path=path))
                # on_load is a generator function then we need to iterate through
                # the generator object.
                if result:
                  for _ in result:
                    yield from render_loop(path=path, init_request=True)
                    runtime().context().set_previous_node_from_current_node()
                    runtime().context().reset_current_node()

          yield from render_loop(path=path)
          runtime().context().set_previous_node_from_current_node()
          runtime().context().reset_current_node()
        yield create_update_state_event(diff=True)
        yield STREAM_END
      else:
        raise Exception(f"Unknown request type: {ui_request}")

    except Exception as e:
      if e in exceptions_to_propagate:
        raise e
      yield from yield_errors(
        error=pb.ServerError(exception=str(e), traceback=format_traceback())
      )

  @flask_app.route("/ui", methods=["POST"])
  def ui_stream() -> Response:
    # Prevent CSRF by checking the request site matches the site
    # of the URL root (where the Flask app is being served from)
    #
    # Skip the check if it's running in debug mode because when
    # running in Colab, the UI and HTTP requests are on different sites.
    if not runtime().debug_mode and not is_same_site(
      request.headers.get("Origin"), request.url_root
    ):
      abort(403, "Rejecting cross-site POST request to /ui")
    data = request.data
    if not data:
      raise Exception("Missing request payload")
    ui_request = pb.UiRequest()
    ui_request.ParseFromString(base64.urlsafe_b64decode(data))

    response = Response(
      stream_with_context(generate_data(ui_request)),
      content_type="text/event-stream",
    )
    return response

  @flask_app.before_request
  def before_request():
    global _requests_in_flight
    _requests_in_flight += 1

  @flask_app.teardown_request
  def teardown(error=None):
    global _requests_in_flight
    _requests_in_flight -= 1

  @flask_app.teardown_request
  def teardown_clear_stale_state_sessions(error=None):
    runtime().context().clear_stale_state_sessions()

  if not prod_mode:

    @flask_app.route("/hot-reload")
    def hot_reload() -> Response:
      counter = int(request.args["counter"])
      while True:
        if counter < runtime().hot_reload_counter:
          break
        # Sleep a short duration but not too short that we hog up excessive CPU.
        time.sleep(0.1)
      response = Response(str(runtime().hot_reload_counter), status=200)
      return response

  return flask_app


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
