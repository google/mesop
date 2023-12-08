import base64
import os

from flask import Flask, Response, request

import optic.protos.ui_pb2 as pb

from optic.runtime import runtime
from optic.exceptions import format_traceback

app = Flask(__name__)


def render_loop(path: str, keep_alive: bool = False):
  try:
    runtime.run_path(path=path)
    root_component = runtime.context().current_node()

    data = pb.UiResponse(
      render=pb.RenderEvent(
        root_component=root_component,
        states=runtime.context().serialize_state(),
      )
    )
    yield serialize(data)
    if not keep_alive:
      yield "data: <stream_end>\n\n"
  except Exception as e:
    print(e)
    yield from yield_errors(
      error=pb.ServerError(exception=str(e), traceback=format_traceback())
    )


def yield_errors(error: pb.ServerError):
  ui_response = pb.UiResponse(error=error)

  yield serialize(ui_response)
  yield "data: <stream_end>\n\n"


def serialize(response: pb.UiResponse) -> str:
  encoded = base64.b64encode(response.SerializeToString()).decode("utf-8")
  return f"data: {encoded}\n\n"


def generate_data(ui_request: pb.UiRequest):
  try:
    runtime.reset_context()

    if runtime.has_loading_errors():
      # Only showing the first error since our error UI only
      # shows one error at a time, and in practice there's usually
      # one error.
      yield from yield_errors(runtime.get_loading_errors()[0])

    if ui_request.HasField("init"):
      yield from render_loop(path=ui_request.path)
    if ui_request.HasField("user_event"):
      result = runtime.context().process_event(ui_request.user_event)
      for _ in result:
        yield from render_loop(path=ui_request.path, keep_alive=True)
        runtime.context().reset_current_node()
      yield "data: <stream_end>\n\n"
    else:
      raise Exception(f"Unknown request type: {ui_request}")

  except Exception as e:
    yield from yield_errors(
      error=pb.ServerError(exception=str(e), traceback=format_traceback())
    )


@app.route("/ui")
def ui_stream():
  param = request.args.get("request", default=None)
  if param is None:
    raise Exception("Missing request parameter")
  ui_request = pb.UiRequest()
  ui_request.ParseFromString(base64.b64decode(param))

  return Response(generate_data(ui_request), content_type="text/event-stream")


port = int(os.environ.get("PORT", 8080))
