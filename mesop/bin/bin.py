import os
import sys
from typing import Sequence

from absl import app, flags

import mesop.protos.ui_pb2 as pb
from mesop.cli.execute_module import execute_module, get_module_name_from_path
from mesop.exceptions import format_traceback
from mesop.runtime import runtime
from mesop.server.wsgi_app import create_app

FLAGS = flags.FLAGS

flags.DEFINE_bool(
  "prod", False, "set to true for prod mode; otherwise editor mode."
)


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

  create_app(
    prod_mode=FLAGS.prod, run_block=lambda: execute_main_module(argv[1])
  ).run()


def execute_main_module(path_arg: str):
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


def make_path_absolute(file_path: str):
  if os.path.isabs(file_path):
    return file_path
  # Otherwise, make the relative path absolute by joining
  # with current working dir.
  absolute_path = os.path.join(os.getcwd(), file_path)
  return absolute_path


def run_main():
  app.run(main)


if __name__ == "__main__":
  run_main()
