import os
from flask import send_from_directory
from .server import app, port
from rules_python.python.runfiles import runfiles  # type: ignore


def get_path():
    r = runfiles.Create()
    return r.Rlocation("optic/web/src/app/prod/web_package")


@app.route("/")
def serve_root():
    return send_from_directory(get_path(), "index.html")


@app.route("/<path:path>")
def serve_file(path: str):
    if is_file_path(path):
        return send_from_directory(get_path(), path)
    else:
        return send_from_directory(get_path(), "index.html")


def run():
    app.run(host="0.0.0.0", port=port, use_reloader=False)


def is_file_path(path: str) -> bool:
    _, last_segment = os.path.split(path)
    return "." in last_segment


if __name__ == "__main__":
    run()
