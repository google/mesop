from typing import Any, Callable

from flask import Flask

from mesop.runtime import enable_debug_mode
from mesop.server.constants import EDITOR_PACKAGE_PATH, PROD_PACKAGE_PATH
from mesop.server.logging import log_startup
from mesop.server.server import configure_flask_app
from mesop.server.static_file_serving import configure_static_file_serving


class App:
  _flask_app: Flask

  def __init__(self, flask_app: Flask):
    self._flask_app = flask_app

  def run(self, port: int = 32123):
    log_startup(port=port)
    self._flask_app.run(host="0.0.0.0", port=port, use_reloader=False)

  def __call__(
    self, environ: dict[Any, Any], start_response: Callable[..., Any]
  ) -> Any:
    """Wrapper around Flask API so that a WGSI server can call this application."""
    return self._flask_app.wsgi_app(environ, start_response)  # type: ignore


def create_app(*, prod_mode: bool = True) -> App:
  flask_app = configure_flask_app()

  if prod_mode:
    enable_debug_mode()

  configure_static_file_serving(
    flask_app,
    static_file_runfiles_base=PROD_PACKAGE_PATH
    if prod_mode
    else EDITOR_PACKAGE_PATH,
  )

  return App(flask_app=flask_app)
