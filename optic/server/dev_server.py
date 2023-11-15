from flask import Response
from .server import app, port


# Disable CORS for development purpose since FE dev server is on a separate origin
# from this server.
@app.after_request
def after_request(response: Response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response


def run():
    app.debug = True
    app.run(host="0.0.0.0", port=port, use_reloader=False)


if __name__ == "__main__":
    run()
