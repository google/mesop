import os
import sys
import threading

from absl import app, flags

import optic.protos.ui_pb2 as pb
from optic.cli.execute_module import execute_module
from optic.exceptions import format_traceback
from optic.runtime import enable_debug_mode, reset_runtime, runtime
from optic.server.flags import port
from optic.server.server import flask_app
from optic.server.static_file_serving import configure_static_file_serving
from optic.utils.runfiles import get_runfile_location

FLAGS = flags.FLAGS

flags.DEFINE_string("path", "", "path to main python module of Optic app.")
flags.DEFINE_bool("debug", False, "set to true for debug mode.")


def monitor_stdin():
  while True:
    line = sys.stdin.readline().strip()
    if line == "IBAZEL_BUILD_COMPLETED SUCCESS":
      reset_runtime()
      execute_module(get_runfile_location(FLAGS.path))


stdin_thread = threading.Thread(target=monitor_stdin)
stdin_thread.daemon = True
stdin_thread.start()


def main(argv):
  if len(FLAGS.path) < 1:
    raise Exception("Required flag 'path'. Received: " + FLAGS.path)

  try:
    execute_module(get_runfile_location(FLAGS.path))
  except Exception as e:
    # Only record error to runtime if in CI mode.
    if FLAGS.debug:
      enable_debug_mode()
      runtime().add_loading_error(
        pb.ServerError(exception=str(e), traceback=format_traceback())
      )
      print("Exception executing module:", e)
    else:
      raise e

  print("Running with hot reload:")

  configure_static_file_serving(
    flask_app,
    static_file_runfiles_base="optic/optic/web/src/app/prod/web_package",
    livereload_script_url=os.environ.get("IBAZEL_LIVERELOAD_URL"),
  )
  flask_app.run(host="0.0.0.0", port=port(), use_reloader=False)


if __name__ == "__main__":
  app.run(main)
