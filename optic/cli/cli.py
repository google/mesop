from absl import app
from absl import flags

from optic.cli.execute_module import execute_module

FLAGS = flags.FLAGS

flags.DEFINE_string("path", "", "path to main python module of Optic app.")


def main(argv):
    if len(FLAGS.path) < 1:
        raise Exception("Required flag 'path'. Received: " + FLAGS.path)

    # Potentially wrap
    execute_module(FLAGS.path)

    print("Running in prod mode")
    from optic.server import prod_server

    prod_server.run()


if __name__ == "__main__":
    app.run(main)
