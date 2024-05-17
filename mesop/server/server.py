import base64
import time
from typing import Generator, Sequence

from flask import Flask, Response, abort, request, stream_with_context

import mesop.protos.ui_pb2 as pb
from mesop.component_helpers import diff_component
from mesop.editor.component_configs import get_component_configs
from mesop.editor.editor_handler import handle_editor_event
from mesop.exceptions import format_traceback
from mesop.runtime import runtime

LOCALHOSTS = (
  # For IPv4 localhost
  "127.0.0.1",
  # For IPv6 localhost
  "::1",
)


def is_processing_request():
  return _requests_in_flight > 0


_requests_in_flight = 0


def configure_flask_app(
  *, prod_mode: bool = True, exceptions_to_propagate: Sequence[type] = ()
) -> Flask:
  flask_app = Flask(__name__)

  def render_loop(
    path: str,
    keep_alive: bool = False,
    trace_mode: bool = False,
    init_request: bool = False,
  ) -> Generator[str, None, None]:
    try:
      runtime().run_path(path=path, trace_mode=trace_mode)

      title = runtime().get_path_title(path=path)

      root_component = runtime().context().current_node()
      previous_root_component = runtime().context().previous_node()
      component_diff = None
      if not trace_mode and previous_root_component:
        component_diff = diff_component(previous_root_component, root_component)
        root_component = None

      data = pb.UiResponse(
        render=pb.RenderEvent(
          root_component=root_component,
          component_diff=component_diff,
          states=runtime().context().serialize_state(),
          commands=runtime().context().commands(),
          component_configs=None
          if prod_mode or not init_request
          else get_component_configs(),
          title=title,
        )
      )
      yield serialize(data)
      if not keep_alive:
        yield "data: <stream_end>\n\n"
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
    yield "data: <stream_end>\n\n"

  def serialize(response: pb.UiResponse) -> str:
    encoded = base64.b64encode(response.SerializeToString()).decode("utf-8")
    return f"data: {encoded}\n\n"

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
        yield from render_loop(path=ui_request.path, init_request=True)
      elif ui_request.HasField("user_event"):
        runtime().context().update_state(ui_request.user_event.states)
        for _ in render_loop(
          path=ui_request.path, keep_alive=True, trace_mode=True
        ):
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
        for _ in result:
          path = ui_request.path
          for command in runtime().context().commands():
            if command.HasField("navigate"):
              path = command.navigate.url
          yield from render_loop(path=path, keep_alive=True)
          runtime().context().set_previous_node_from_current_node()
          runtime().context().reset_current_node()
        yield "data: <stream_end>\n\n"
      elif ui_request.HasField("editor_event"):
        # Prevent accidental usages of editor mode outside of
        # one's local computer
        if request.remote_addr not in LOCALHOSTS:
          abort(403)  # Throws a Forbidden Error
        # Visual editor should only be enabled in debug mode.
        if not runtime().debug_mode:
          abort(403)  # Throws a Forbidden Error
        handle_editor_event(ui_request.editor_event)
        yield "data: <stream_end>\n\n"
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
