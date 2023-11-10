import base64
from flask import Flask, Response

import protos.ui_pb2 as pb

from optic.lib.runtime import runtime

app = Flask(__name__)


def generate_data():
    runtime.run_module()
    root_component = runtime.session().current_node()
    
    # TODO: reset session.

    data = pb.ServerEvent(
        render=pb.RenderEvent(
            root_component=root_component
        )
    )
    encodedString = base64.b64encode(data.SerializeToString()).decode('utf-8')

    return f"data: {encodedString}\n\n"


@app.route("/ui")
def ui_stream():
    return Response(generate_data(), content_type="text/event-stream")
