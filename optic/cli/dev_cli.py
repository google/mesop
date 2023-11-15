from absl import app
from absl import flags

from optic.lib.runtime import runtime
from optic.cli.read_module import read_module

FLAGS = flags.FLAGS

flags.DEFINE_string("path", "", "path to main python module of Optic app.")


def main(argv):
    if len(FLAGS.path) < 1:
        raise Exception("Required flag 'path'. Received: " + FLAGS.path)

    runtime.set_load_module(lambda: read_module(FLAGS.path))

    print("Running in dev mode")
    from optic.server import dev_server

    dev_server.run()


if __name__ == "__main__":
    app.run(main)
