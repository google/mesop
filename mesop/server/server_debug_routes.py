import inspect
import json
import time
from urllib import request as urllib_request
from urllib.error import URLError

from flask import Flask, Response, request

from mesop.env.env import AI_SERVICE_BASE_URL
from mesop.runtime import runtime
from mesop.server.server_utils import (
  check_editor_access,
  make_sse_response,
  sse_request,
)


def configure_debug_routes(flask_app: Flask):
  @flask_app.route("/__editor__/commit", methods=["POST"])
  def page_commit() -> Response:
    check_editor_access()

    try:
      data = request.get_json()
    except json.JSONDecodeError:
      return Response("Invalid JSON format", status=400)
    code = data.get("code")
    path = data.get("path")
    page_config = runtime().get_page_config(path=path)
    assert page_config
    module = inspect.getmodule(page_config.page_fn)
    assert module
    module_file = module.__file__
    assert module_file
    module_file_path = module.__file__
    assert module_file_path
    with open(module_file_path, "w") as file:
      file.write(code)

    response_data = {"message": "Page commit successful"}
    return Response(
      json.dumps(response_data), status=200, mimetype="application/json"
    )

  @flask_app.route("/__editor__/save-interaction", methods=["POST"])
  def save_interaction() -> Response | dict[str, str]:
    check_editor_access()

    data = request.get_json()
    if not data:
      return Response("Invalid JSON data", status=400)

    try:
      req = urllib_request.Request(
        AI_SERVICE_BASE_URL + "/save-interaction",
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
      )
      with urllib_request.urlopen(req) as response:
        if response.status == 200:
          folder = json.loads(response.read().decode("utf-8"))["folder"]
          return {"folder": folder}
        else:
          print(f"Error from AI service: {response.read().decode('utf-8')}")
          return Response(
            f"Error from AI service: {response.read().decode('utf-8')}",
            status=500,
          )
    except URLError as e:
      return Response(f"Error making request to AI service: {e!s}", status=500)

  @flask_app.route("/__editor__/generate", methods=["POST"])
  def page_generate():
    check_editor_access()

    try:
      data = request.get_json()
    except json.JSONDecodeError:
      return Response("Invalid JSON format", status=400)
    if not data:
      return Response("Invalid JSON data", status=400)

    prompt = data.get("prompt")
    if not prompt:
      return Response("Missing 'prompt' in JSON data", status=400)

    path = data.get("path")
    page_config = runtime().get_page_config(path=path)

    line_number = data.get("lineNumber")
    assert page_config
    module = inspect.getmodule(page_config.page_fn)
    if module is None:
      return Response("Could not retrieve module source code.", status=500)
    module_file = module.__file__
    assert module_file
    with open(module_file) as file:
      source_code = file.read()
    print(f"Source code of module {module.__name__}:")

    def generate():
      try:
        for event in sse_request(
          AI_SERVICE_BASE_URL + "/adjust-mesop-app",
          {"prompt": prompt, "code": source_code, "lineNumber": line_number},
        ):
          if event.get("type") == "end":
            sse_data = {
              "type": "end",
              "prompt": prompt,
              "path": path,
              "beforeCode": source_code,
              "afterCode": event["code"],
              "diff": event["diff"],
              "message": "Prompt processed successfully",
            }
            yield f"data: {json.dumps(sse_data)}\n\n"
            break
          elif event.get("type") == "progress":
            sse_data = {"data": event["data"], "type": "progress"}
            yield f"data: {json.dumps(sse_data)}\n\n"
          elif event.get("type") == "error":
            sse_data = {"error": event["error"], "type": "error"}
            yield f"data: {json.dumps(sse_data)}\n\n"
            break
          else:
            raise Exception(f"Unknown event type: {event}")
      except Exception as e:
        sse_data = {
          "error": "Could not connect to AI service: " + str(e),
          "type": "error",
        }
        yield f"data: {json.dumps(sse_data)}\n\n"

    return make_sse_response(generate())

  @flask_app.route("/__hot-reload__")
  def hot_reload() -> Response:
    counter = int(request.args["counter"])
    while True:
      if counter < runtime().hot_reload_counter:
        break
      # Sleep a short duration but not too short that we hog up excessive CPU.
      time.sleep(0.1)
    response = Response(str(runtime().hot_reload_counter), status=200)
    return response
