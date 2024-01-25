import logging
import os
import sys
import threading

from absl import app, flags

import mesop.protos.ui_pb2 as pb
from mesop.cli.execute_module import execute_module
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

FLAGS = flags.FLAGS

flags.DEFINE_string("path", "", "path to main python module of Mesop app.")
flags.DEFINE_bool(
  "prod", False, "set to true for prod mode; otherwise editor mode."
)
flags.DEFINE_bool("verbose", False, "set to true for verbose logging.")


def monitor_stdin():
  while True:
    line = sys.stdin.readline().strip()
    if line == "IBAZEL_BUILD_COMPLETED SUCCESS":
      logging.log(logging.INFO, "ibazel build complete; starting hot reload")
      try:
        reset_runtime()
        execute_module(runfile_path=FLAGS.path)
        hot_reload_finished()
      except Exception as e:
        logging.log(
          logging.ERROR, "Could not hot reload due to error:", exc_info=e
        )


def main(argv):
  flask_app = configure_flask_app()
  if len(FLAGS.path) < 1:
    raise Exception("Required flag 'path'. Received: " + FLAGS.path)

  if not FLAGS.prod:
    enable_debug_mode()
    stdin_thread = threading.Thread(
      target=monitor_stdin, name="mesop_build_watcher_thread"
    )
    stdin_thread.daemon = True
    stdin_thread.start()

  try:
    execute_module(runfile_path=FLAGS.path)
  except Exception as e:
    # Only record error to runtime if in CI mode.
    if not FLAGS.prod:
      runtime().add_loading_error(
        pb.ServerError(exception=str(e), traceback=format_traceback())
      )
      print("Exception executing module:", e)
    else:
      raise e

  print("Running with hot reload:")

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
    log_startup()
    logging.getLogger("werkzeug").setLevel(logging.WARN)

  flask_app.run(host="0.0.0.0", port=port(), use_reloader=False)


if __name__ == "__main__":
  app.run(main)
