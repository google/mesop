from flask import Flask, Response
import time
import json

import protos.ui_pb2 as pb


app = Flask(__name__)

def generate_data():
    """
    This generator yields data in a streaming fashion which will be sent to the client.
    For demonstration purposes, it sends JSON-encoded data, which includes a message and a timestamp.
    """
    count = 0
    while True:
        time.sleep(1)  # Simulate a delay for data preparation
        count += 1
        uir = pb.UiResponse(id=count)
        data = json.dumps({'time': time.time(), 'message': f'Data number {uir.SerializeToString()}'})
        yield f"data: {data}\n\n"

@app.route('/ui')
def ui_stream():
    """
    This view function is the SSE endpoint. It returns a streaming response that
    yields data from the generator function.
    """
    return Response(generate_data(), content_type='text/event-stream')