import gzip
import io
import os
from io import BytesIO
from typing import Any, Callable

from flask import Flask, send_file
from werkzeug.security import safe_join

from mesop.utils.runfiles import get_runfile_location


def noop():
  pass


def configure_static_file_serving(
  app: Flask,
  static_file_runfiles_base: str,
  livereload_script_url: str | None = None,
  preprocess_request: Callable[[], None] = noop,
):
  def get_path(path: str):
    safe_path = safe_join(static_file_runfiles_base, path)
    assert safe_path
    return get_runfile_location(safe_path)

  def retrieve_index_html() -> io.BytesIO | str:
    if livereload_script_url:
      file_path = get_path("index.html")
      with open(file_path) as file:
        lines = file.readlines()

      for i, line in enumerate(lines):
        if line.strip() == "<!-- Inject script (if needed) -->":
          lines[i] = f'<script src="{livereload_script_url}"></script>\n'

      # Create a BytesIO object from the modified lines
      modified_file_content = "".join(lines)
      binary_file = io.BytesIO(modified_file_content.encode())

      return binary_file
    return get_path("index.html")

  @app.route("/")
  def serve_root():
    preprocess_request()
    return send_file(retrieve_index_html(), download_name="index.html")

  @app.route("/<path:path>")
  def serve_file(path: str):
    preprocess_request()
    if is_file_path(path):
      return send_file_compressed(get_path(path))
    else:
      return send_file(retrieve_index_html(), download_name="index.html")


def is_file_path(path: str) -> bool:
  _, last_segment = os.path.split(path)
  return "." in last_segment


# To avoid paying the cost of gzipping the same file multiple times
# we have a singleton cache from file path to gzipped bytes.
gzip_cache: dict[str, bytes] = {}


def send_file_compressed(path: str) -> Any:
  response = send_file(path)
  response.headers["Content-Encoding"] = "gzip"
  response.direct_passthrough = False
  if path in gzip_cache:
    gzip_data = gzip_cache[path]
  else:
    gzip_buffer = BytesIO()
    with gzip.GzipFile(
      mode="wb", fileobj=gzip_buffer, compresslevel=6
    ) as gzip_file:
      gzip_file.write(response.get_data())
    gzip_buffer.seek(0)
    gzip_data = gzip_buffer.getvalue()
    gzip_cache[path] = gzip_data

  response.set_data(gzip_data)
  response.headers["Content-Length"] = str(len(response.get_data()))
  return response
