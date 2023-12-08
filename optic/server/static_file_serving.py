import os

from flask import Flask, send_file
from werkzeug.security import safe_join

from optic.utils.runfiles import get_runfile_location


def configure_static_file_serving(app: Flask, static_file_runfiles_base: str):
  def get_path(path: str):
    safe_path = safe_join(static_file_runfiles_base, path)
    assert safe_path
    return get_runfile_location(safe_path)

  @app.route("/")
  def serve_root():
    return send_file(get_path("index.html"))

  @app.route("/<path:path>")
  def serve_file(path: str):
    if is_file_path(path):
      return send_file(get_path(path))
    else:
      return send_file(get_path("index.html"))


def is_file_path(path: str) -> bool:
  _, last_segment = os.path.split(path)
  return "." in last_segment
