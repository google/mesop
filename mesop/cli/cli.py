import logging
import os
import sys
import threading
from typing import Sequence

from absl import app, flags

import mesop.protos.ui_pb2 as pb
from mesop.cli.execute_module import (
  execute_module,
  get_module_name_from_runfile_path,
)
from mesop.exceptions import format_traceback
from mesop.runtime import (
  enable_debug_mode,
  hot_reload_finished,
  reset_runtime,
  runtime,
)
from mesop.server.constants import EDITOR_PACKAGE_PATH, PROD_PACKAGE_PATH
from mesop.server.flags import port
from mesop.server.logging import log_startup
from mesop.server.server import configure_flask_app
from mesop.server.static_file_serving import configure_static_file_serving
from mesop.utils.runfiles import get_runfile_location

FLAGS = flags.FLAGS

flags.DEFINE_string("path", "", "path to main python module of Mesop app.")
flags.DEFINE_bool(
  "prod", False, "set to true for prod mode; otherwise editor mode."
)
flags.DEFINE_bool("verbose", False, "set to true for verbose logging.")


def execute_main_module():
  execute_module(
    module_path=get_runfile_location(FLAGS.path),
    module_name=get_module_name_from_runfile_path(FLAGS.path),
  )


def monitor_stdin():
  while True:
    line = sys.stdin.readline().strip()
    if line == "IBAZEL_BUILD_COMPLETED SUCCESS":
      logging.log(logging.INFO, "ibazel build complete; starting hot reload")
      try:
        reset_runtime()
        execute_main_module()
        hot_reload_finished()
      except Exception as e:
        logging.log(
          logging.ERROR, "Could not hot reload due to error:", exc_info=e
        )


def main(argv: Sequence[str]):
  flask_app = configure_flask_app()
  if len(FLAGS.path) < 1:
    raise Exception("Required flag 'path'. Received: " + FLAGS.path)

  if not FLAGS.prod:
    enable_debug_mode()

  try:
    execute_main_module()
  except Exception as e:
    # Only record error to runtime if in CI mode.
    if not FLAGS.prod:
      runtime().add_loading_error(
        pb.ServerError(exception=str(e), traceback=format_traceback())
      )
      print("Exception executing module:", e)
    else:
      raise e

  # WARNING: this needs to run *after* the initial `execute_module`
  # has completed, otherwise there's a potential race condition where the
  # background thread and main thread are running `execute_module` which
  # leads to obscure hot reloading bugs.
  if not FLAGS.prod:
    print("Running with hot reload:")
    stdin_thread = threading.Thread(
      target=monitor_stdin, name="mesop_build_watcher_thread"
    )
    stdin_thread.daemon = True
    stdin_thread.start()

  configure_static_file_serving(
    flask_app,
    static_file_runfiles_base=PROD_PACKAGE_PATH
    if FLAGS.prod
    else EDITOR_PACKAGE_PATH,
    livereload_script_url=os.environ.get("IBAZEL_LIVERELOAD_URL"),
  )

  if FLAGS.verbose:
    logging.getLogger("werkzeug").setLevel(logging.INFO)
  else:
    log_startup(port=port())
    logging.getLogger("werkzeug").setLevel(logging.WARN)

  flask_app.run(host="::", port=port(), use_reloader=False)


if __name__ == "__main__":
  app.run(main)
