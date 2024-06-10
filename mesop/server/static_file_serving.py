import gzip
import io
import os
import re
import secrets
from collections import OrderedDict
from io import BytesIO
from typing import Any, Callable

from flask import Flask, Response, g, request, send_file
from werkzeug.security import safe_join

from mesop.runtime import runtime
from mesop.utils.runfiles import get_runfile_location


def noop():
  pass


def configure_static_file_serving(
  app: Flask,
  static_file_runfiles_base: str,
  livereload_script_url: str | None = None,
  preprocess_request: Callable[[], None] = noop,
  disable_gzip_cache: bool = False,
  default_allowed_iframe_parents: str = "'self'",
):
  def get_path(path: str):
    safe_path = safe_join(static_file_runfiles_base, path)
    assert safe_path
    return get_runfile_location(safe_path)

  def retrieve_index_html() -> io.BytesIO | str:
    page_config = runtime().get_page_config(path=request.path)
    file_path = get_path("index.html")
    with open(file_path) as file:
      lines = file.readlines()

    for i, line in enumerate(lines):
      if "$$INSERT_CSP_NONCE$$" in line:
        lines[i] = lines[i].replace("$$INSERT_CSP_NONCE$$", g.csp_nonce)
      if (
        livereload_script_url
        and line.strip() == "<!-- Inject script (if needed) -->"
      ):
        lines[i] = (
          f'<script src="{livereload_script_url}" nonce={g.csp_nonce}></script>\n'
        )

      if (
        page_config
        and page_config.stylesheets
        and line.strip() == "<!-- Inject stylesheet (if needed) -->"
      ):
        lines[i] = "\n".join(
          [
            f'<link href="{stylesheet}" rel="stylesheet">'
            for stylesheet in page_config.stylesheets
          ]
        )

    # Create a BytesIO object from the modified lines
    modified_file_content = "".join(lines)
    binary_file = io.BytesIO(modified_file_content.encode())

    return binary_file

  @app.route("/")
  def serve_root():
    preprocess_request()
    return send_file(retrieve_index_html(), download_name="index.html")

  @app.route("/<path:path>")
  def serve_file(path: str):
    preprocess_request()
    if is_file_path(path):
      return send_file_compressed(
        get_path(path),
        disable_gzip_cache=disable_gzip_cache,
      )
    else:
      return send_file(retrieve_index_html(), download_name="index.html")

  @app.before_request
  def generate_nonce():
    g.csp_nonce = secrets.token_urlsafe(16)

  @app.after_request
  def add_security_headers(response: Response):
    page_config = runtime().get_page_config(path=request.path)
    # Set X-Content-Type-Options header to prevent MIME type sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"

    # Set Strict-Transport-Security header to enforce HTTPS
    # All present and future subdomains will be HTTPS for a max-age of 1 year.
    # This blocks access to pages or subdomains that can only be served over HTTP.
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security#examples
    response.headers["Strict-Transport-Security"] = (
      "max-age=31536000; includeSubDomains"
    )

    # Technically order doesn't matter, but it's useful for testing
    # https://stackoverflow.com/a/77850553
    csp = OrderedDict(
      {
        "default-src": "'self'",
        "font-src": "fonts.gstatic.com",
        # Mesop app developers should be able to iframe other sites.
        "frame-src": "'self' https:",
        # Mesop app developers should be able to load images and media from various origins.
        "img-src": "'self' data: https: http:",
        "media-src": "'self' data: https:",
        "style-src": f"'self' 'nonce-{g.csp_nonce}' fonts.googleapis.com",
        # Need 'unsafe-inline' because we apply inline styles for our components.
        # This is also used by Angular for animations:
        # https://github.com/angular/angular/pull/55260
        "style-src-attr": "'unsafe-inline'",
        "script-src": f"'self' 'nonce-{g.csp_nonce}'",
        # https://angular.io/guide/security#enforcing-trusted-types
        "trusted-types": "angular angular#unsafe-bypass",
        "require-trusted-types-for": "'script'",
      }
    )
    if runtime().debug_mode:
      # Allow all origins in debug mode (aka editor mode) because
      # when Mesop is running under Colab, it will be served from
      # a randomly generated origin.
      csp["frame-ancestors"] = "*"
    elif page_config and page_config.security_policy.allowed_iframe_parents:
      csp["frame-ancestors"] = "'self' " + " ".join(
        list(page_config.security_policy.allowed_iframe_parents)
      )
    else:
      csp["frame-ancestors"] = default_allowed_iframe_parents

    if livereload_script_url:
      livereload_origin = extract_origin(livereload_script_url)
      if livereload_origin:
        csp["connect-src"] = f"'self' {livereload_origin}"

    # Set Content-Security-Policy header to restrict resource loading
    # Based on https://angular.io/guide/security#content-security-policy
    response.headers["Content-Security-Policy"] = "; ".join(
      [key + " " + value for key, value in csp.items()]
    )

    # Set Referrer-Policy header to control referrer information
    # Recommended by https://web.dev/articles/referrer-best-practices
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    # If we've set Cache-Control earlier, respect those.
    if "Cache-Control" not in response.headers:
      # no-store ensures that resources are never cached.
      # https://web.dev/articles/http-cache#request-headers
      response.headers["Cache-Control"] = "no-store"

    return response


def is_file_path(path: str) -> bool:
  _, last_segment = os.path.split(path)
  return "." in last_segment


# To avoid paying the cost of gzipping the same file multiple times
# we have a singleton cache from file path to gzipped bytes.
gzip_cache: dict[str, bytes] = {}


def send_file_compressed(path: str, disable_gzip_cache: bool) -> Any:
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
    if not disable_gzip_cache:
      gzip_cache[path] = gzip_data

  response.set_data(gzip_data)
  response.headers["Content-Length"] = str(len(response.get_data()))
  return response


def extract_origin(livereload_script_url: str) -> str | None:
  match = re.search(r"localhost:\d+", livereload_script_url)
  if match:
    return match.group()
  # If we couldn't extract an origin, return None
  return None
