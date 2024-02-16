import base64
from typing import Generator, Sequence

from flask import Flask, Response, abort, request, stream_with_context

import mesop.protos.ui_pb2 as pb
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


def configure_flask_app(
  *, exceptions_to_propagate: Sequence[type] = ()
) -> Flask:
  flask_app = Flask(__name__)

  def render_loop(
    path: str, keep_alive: bool = False, trace_mode: bool = False
  ) -> Generator[str, None, None]:
    try:
      runtime().run_path(path=path, trace_mode=trace_mode)
      title = runtime().get_path_title(path=path)
      root_component = runtime().context().current_node()

      data = pb.UiResponse(
        render=pb.RenderEvent(
          root_component=root_component,
          states=runtime().context().serialize_state(),
          commands=runtime().context().commands(),
          component_configs=get_component_configs(),
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
        yield from render_loop(path=ui_request.path)
      elif ui_request.HasField("user_event"):
        runtime().context().update_state(ui_request.user_event.states)
        for _ in render_loop(
          path=ui_request.path, keep_alive=True, trace_mode=True
        ):
          runtime().context().reset_current_node()
          pass
        result = runtime().context().run_event_handler(ui_request.user_event)
        for _ in result:
          path = ui_request.path
          for command in runtime().context().commands():
            if command.HasField("navigate"):
              path = command.navigate.url
          yield from render_loop(path=path, keep_alive=True)
          runtime().context().reset_current_node()
        yield "data: <stream_end>\n\n"
      elif ui_request.HasField("editor_event"):
        # Prevent accidental usages of editor mode outside of
        # one's local computer
        if request.remote_addr not in LOCALHOSTS:
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

    return Response(
      stream_with_context(generate_data(ui_request)),
      content_type="text/event-stream",
    )

  return flask_app
