import logging
import os
import sys
import threading
import time
from typing import Sequence

from absl import app, flags

import mesop.protos.ui_pb2 as pb
from mesop.cli.execute_module import execute_module, get_module_name_from_path
from mesop.exceptions import format_traceback
from mesop.runtime import (
  enable_debug_mode,
  hot_reload_finished,
  reset_runtime,
  runtime,
)
from mesop.server.server import is_processing_request
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

  if not FLAGS.prod:
    enable_debug_mode()

  absolute_path = absolute_path = make_path_absolute(argv[1])
  app = create_app(
    prod_mode=FLAGS.prod,
    run_block=lambda: execute_main_module(absolute_path=absolute_path),
  )

  # WARNING: this needs to run *after* the initial `execute_module`
  # has completed, otherwise there's a potential race condition where the
  # background thread and main thread are running `execute_module` which
  # leads to obscure hot reloading bugs.
  if not FLAGS.prod:
    print("Running with hot reload:")
    stdin_thread = threading.Thread(
      target=lambda: fs_watcher(absolute_path), name="mesop_fs_watcher_thread"
    )
    stdin_thread.daemon = True
    stdin_thread.start()

  logging.getLogger("werkzeug").setLevel(logging.WARN)
  app.run()


def fs_watcher(absolute_path: str):
  """
  Naive filesystem watcher for the main module of the Mesop application.

  In the future, we can watch for the entire directory, but this captures the main 80% case.
  """
  last_modified = os.path.getmtime(absolute_path)
  while True:
    # Get the current modification time
    current_modified = os.path.getmtime(absolute_path)

    # Compare the current modification time with the last modification time
    if current_modified != last_modified and not is_processing_request():
      # Update the last modification time
      last_modified = current_modified
      try:
        print("Hot reload: starting...")
        reset_runtime()
        execute_main_module(absolute_path=absolute_path)
        hot_reload_finished()
        print("Hot reload: finished!")
      except Exception as e:
        logging.log(
          logging.ERROR, "Could not hot reload due to error:", exc_info=e
        )

    time.sleep(0.1)


def execute_main_module(absolute_path: str):
  try:
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
