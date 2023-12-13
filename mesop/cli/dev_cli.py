from absl import app, flags

import mesop.protos.ui_pb2 as pb
from mesop.cli.execute_module import execute_module
from mesop.exceptions import format_traceback
from mesop.runtime import enable_debug_mode, runtime
from mesop.server import dev_server
from mesop.server.flags import port
from mesop.server.server import flask_app
from mesop.utils.runfiles import get_runfile_location

FLAGS = flags.FLAGS

flags.DEFINE_string("path", "", "path to main python module of Mesop app.")


def main(argv):
  if len(FLAGS.path) < 1:
    raise Exception("Required flag 'path'. Received: " + FLAGS.path)

  enable_debug_mode()

  try:
    execute_module(get_runfile_location(FLAGS.path))
  except Exception as e:
    runtime().add_loading_error(
      pb.ServerError(exception=str(e), traceback=format_traceback())
    )
    print("Exception executing module:", e)

  print("Starting dev server...")
  dev_server.configure_dev_server(flask_app)
  flask_app.debug = True
  flask_app.run(host="0.0.0.0", port=port(), use_reloader=False)


if __name__ == "__main__":
  app.run(main)
