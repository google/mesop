import sys
from typing import Any, Callable

from absl import flags
from flask import Flask

from mesop.runtime import enable_debug_mode
from mesop.server.constants import EDITOR_PACKAGE_PATH, PROD_PACKAGE_PATH
from mesop.server.flags import port
from mesop.server.logging import log_startup
from mesop.server.server import configure_flask_app
from mesop.server.static_file_serving import configure_static_file_serving
from mesop.utils.host_util import get_default_host


class App:
  _flask_app: Flask

  def __init__(self, flask_app: Flask):
    self._flask_app = flask_app

  def run(self):
    log_startup(port=port())
    self._flask_app.run(
      host=get_default_host(), port=port(), use_reloader=False
    )


def create_app(
  prod_mode: bool,
  run_block: Callable[..., None] | None = None,
) -> App:
  flask_app = configure_flask_app(prod_mode=prod_mode)

  if not prod_mode:
    enable_debug_mode()

  if run_block is not None:
    run_block()

  configure_static_file_serving(
    flask_app,
    static_file_runfiles_base=PROD_PACKAGE_PATH
    if prod_mode
    else EDITOR_PACKAGE_PATH,
    disable_gzip_cache=not prod_mode,
  )

  return App(flask_app=flask_app)


def create_wsgi_app(*, debug_mode: bool = False):
  _app = None

  def wsgi_app(environ: dict[Any, Any], start_response: Callable[..., Any]):
    nonlocal _app
    if not _app:
      flags.FLAGS(sys.argv[:1])
      _app = create_app(prod_mode=not debug_mode)

    return _app._flask_app.wsgi_app(environ, start_response)  # type: ignore

  return wsgi_app
