import base64
from flask import Flask, Response, request

import protos.ui_pb2 as pb

from optic.lib.runtime import runtime

app = Flask(__name__)


def generate_data(ui_request: pb.UiRequest):
    if ui_request.HasField("init"):
        runtime.run_module()
        root_component = runtime.session().current_node()

        data = pb.ServerEvent(render=pb.RenderEvent(root_component=root_component))

        runtime.reset_session()

        encodedString = base64.b64encode(data.SerializeToString()).decode("utf-8")

        yield f"data: {encodedString}\n\n"
        yield "data: <stream_end>\n\n"
    elif ui_request.HasField("user_action"):
        print("ui_action=", ui_request.user_action)
        yield "data: <stream_end>\n\n"
        pass
    else:
        raise Exception(f"Unknown request type: {ui_request}")


@app.route("/ui")
def ui_stream():
    param = request.args.get("request", default=None)
    ui_request = pb.UiRequest(init=pb.InitRequest())
    if param is not None:
        ui_request = pb.UiRequest()
        ui_request.ParseFromString(base64.b64decode(param))

    return Response(generate_data(ui_request), content_type="text/event-stream")
