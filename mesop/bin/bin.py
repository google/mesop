import os
import sys
from typing import Any, Callable, Sequence

from absl import app, flags
from flask import Flask

import mesop.protos.ui_pb2 as pb
from mesop.cli.execute_module import execute_module, get_module_name_from_path
from mesop.exceptions import format_traceback
from mesop.runtime import enable_debug_mode, runtime
from mesop.server.constants import EDITOR_PACKAGE_PATH, PROD_PACKAGE_PATH
from mesop.server.flags import port
from mesop.server.logging import log_startup
from mesop.server.server import configure_flask_app
from mesop.server.static_file_serving import configure_static_file_serving

FLAGS = flags.FLAGS

flags.DEFINE_bool(
  "prod", False, "set to true for prod mode; otherwise editor mode."
)
flags.DEFINE_bool("verbose", False, "set to true for verbose logging.")


class App:
  _flask_app: Flask

  def __init__(self, flask_app: Flask):
    self._flask_app = flask_app

  def run(self):
    log_startup(port=port())
    self._flask_app.run(host="0.0.0.0", port=port(), use_reloader=False)

  def __call__(
    self, environ: dict[Any, Any], start_response: Callable[..., Any]
  ) -> Any:
    """Wrapper around Flask API so that a WGSI server can call this application."""
    return self._flask_app.wsgi_app(environ, start_response)  # type: ignore


def make_path_absolute(file_path: str):
  if os.path.isabs(file_path):
    return file_path
  # Otherwise, make the relative path absolute by joining
  # with current working dir.
  absolute_path = os.path.join(os.getcwd(), file_path)
  return absolute_path


def create_app(path_arg: str) -> App:
  flask_app = configure_flask_app()

  if FLAGS.prod:
    enable_debug_mode()

  try:
    absolute_path = make_path_absolute(path_arg)
    execute_module(
      module_path=absolute_path,
      module_name=get_module_name_from_path(absolute_path),
    )
  except Exception as e:
    if not FLAGS.prod:
      runtime().add_loading_error(
        pb.ServerError(exception=str(e), traceback=format_traceback())
      )
    # Always raise an error to make it easy to debug
    raise e

  configure_static_file_serving(
    flask_app,
    static_file_runfiles_base=PROD_PACKAGE_PATH
    if FLAGS.prod
    else EDITOR_PACKAGE_PATH,
  )

  return App(flask_app=flask_app)


def main(argv: Sequence[str]):
  if len(argv) < 2:
    print(
      """\u001b[31mERROR: missing command-line argument to Mesop application.\u001b[0m

Example command:
$\u001b[35m mesop file.py\u001b[0m"""
    )
    sys.exit(1)

  if len(argv) > 2:
    print(
      f"""\u001b[31mERROR: Too many command-line arguments.\u001b[0m

Actual:
$\u001b[35m mesop {" ".join(argv[1:])}\u001b[0m

Re-run with:
$\u001b[35m mesop {argv[1]}\u001b[0m"""
    )
    sys.exit(1)
  create_app(argv[1]).run()


def run_main():
  app.run(main)


if __name__ == "__main__":
  run_main()
