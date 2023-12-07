from absl import app
from absl import flags

import optic.protos.ui_pb2 as pb
from optic.cli.execute_module import execute_module
from optic.exceptions import format_traceback

FLAGS = flags.FLAGS

flags.DEFINE_string("path", "", "path to main python module of Optic app.")
flags.DEFINE_bool("debug", False, "set to true for debug mode.")


def main(argv):
    if len(FLAGS.path) < 1:
        raise Exception("Required flag 'path'. Received: " + FLAGS.path)

    try:
        execute_module(FLAGS.path)
    except Exception as e:
        # Only record error to runtime if in CI mode.
        if FLAGS.debug:
            from optic.runtime import runtime

            runtime.add_loading_error(
                pb.ServerError(exception=str(e), traceback=format_traceback())
            )
            print("Exception executing module:", e)
        else:
            raise e

    print("Running in prod mode")
    from optic.server import prod_server

    prod_server.run()


if __name__ == "__main__":
    app.run(main)
