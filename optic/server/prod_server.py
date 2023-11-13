from flask import send_from_directory
from .server import app

import os

def get_path():
    return os.path.join(os.getcwd(), "web/src/app/web_package")

@app.route("/")
def serve_root():
    return send_from_directory(get_path(), "index.html")


@app.route("/<path:path>")
def serve_file(path: str):
    return send_from_directory(get_path(), path)


def run():
    app.run(host="0.0.0.0", port=8080, use_reloader=False)


if __name__ == "__main__":
    run()
