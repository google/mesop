import logging
import os
import sys
import threading
import time
from typing import Sequence, cast

from absl import app, flags
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

import mesop.protos.ui_pb2 as pb
from mesop.cli.execute_module import execute_module, get_module_name_from_path
from mesop.exceptions import format_traceback
from mesop.runtime import (
  enable_debug_mode,
  hot_reload_finished,
  reset_runtime,
  runtime,
)
from mesop.server.wsgi_app import create_app

FLAGS = flags.FLAGS

flags.DEFINE_bool(
  "prod", False, "set to true for prod mode; otherwise editor mode."
)


def main(argv: Sequence[str]):
  if len(argv) < 2:
    print(
      """\u001b[31mERROR: missing command-line argument to Mesop.\u001b[0m

Example run command:
$\u001b[35m mesop file.py\u001b[0m"""
    )
    sys.exit(1)

  if argv[1] == "init":
    if len(argv) > 3:
      print(
        f"""\u001b[31mERROR: Too many command-line arguments for mesop init.\u001b[0m

Actual:
$\u001b[35m mesop {" ".join(argv[1:])}\u001b[0m

Re-run with:
$\u001b[35m mesop init file.py\u001b[0m"""
      )
      sys.exit(1)

    filename = argv[2] if len(argv) == 3 else "main.py"
    absolute_path = make_path_absolute(filename)
    if os.path.isfile(absolute_path):
      print(f"\u001b[31mERROR: {filename} already exists.\u001b[0m")
      sys.exit(1)
    with open(
      os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../examples/starter_kit/starter_kit.py",
      )
    ) as src_file:
      with open(absolute_path, "w") as dest_file:
        dest_file.write(src_file.read().replace("/starter_kit", "/"))
    print(f"""Created starter kit Mesop app at {filename} 🎉

Run Mesop app:
$\u001b[35m mesop {filename}\u001b[0m
""")
    sys.exit(0)
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

  absolute_path = make_path_absolute(argv[1])

  # If you run `$ python /path/to/script.py`, Python will add
  # "/path/to" to sys.path.
  #
  # Running `$ mesop /path/to/script.py` should mimic this behavior
  # so that imports work as expected (e.g. https://github.com/google/mesop/issues/128)
  #
  # Ref:
  # https://docs.python.org/3/library/sys_path_init.html
  sys.path = [os.path.dirname(absolute_path), *sys.path]

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


app_modules: set[str] = set()


def clear_app_modules() -> None:
  # Remove labs modules because they function as application code
  # and it needs to be re-executed so that their stateclass is
  # re-registered b/c the runtime is reset.
  labs_modules: set[str] = set()
  for module in sys.modules:
    if module.startswith("mesop.labs"):
      # Do not delete the module directly, because this causes
      # an error where the dictionary size is changed during iteration.
      labs_modules.add(module)
  for module in labs_modules:
    del sys.modules[module]

  for module in app_modules:
    # Not every module has been loaded into sys.modules (e.g. the main module)
    if module in sys.modules:
      del sys.modules[module]


def add_app_module(workspace_dir_path: str, app_module_path: str) -> None:
  module_name = get_app_module_name(
    workspace_dir_path=workspace_dir_path, app_module_path=app_module_path
  )
  app_modules.add(module_name)


def remove_app_module(workspace_dir_path: str, app_module_path: str) -> None:
  module_name = get_app_module_name(
    workspace_dir_path=workspace_dir_path, app_module_path=app_module_path
  )
  app_modules.remove(module_name)


def get_app_module_name(workspace_dir_path: str, app_module_path: str) -> str:
  relative_path = os.path.relpath(app_module_path, workspace_dir_path)

  return (
    relative_path.replace(os.sep, ".")
    # Special case __init__.py:
    # e.g. foo.bar.__init__.py -> foo.bar
    # Otherwise, remove the ".py" suffix
    .removesuffix(".__init__.py")
    .removesuffix(".py")
  )


class ReloadEventHandler(FileSystemEventHandler):
  def __init__(self, absolute_path: str, workspace_dir_path: str):
    self.count = 0
    self.absolute_path = absolute_path
    self.workspace_dir_path = workspace_dir_path

  def on_modified(self, event: FileSystemEvent):
    src_path = cast(str, event.src_path)
    # This could potentially over-trigger if .py files which are
    # not application modules are modified (e.g. in venv directories)
    # but this should be rare.
    if src_path.endswith(".py"):
      try:
        self.count += 1
        print(f"Hot reload #{self.count}: starting...")
        reset_runtime()
        execute_main_module(absolute_path=self.absolute_path)
        hot_reload_finished()
        print(f"Hot reload #{self.count}: finished!")
      except Exception as e:
        logging.log(
          logging.ERROR, "Could not hot reload due to error:", exc_info=e
        )

  def on_created(self, event: FileSystemEvent):
    src_path = cast(str, event.src_path)
    if src_path.endswith(".py"):
      print(f"Watching new Python module: {event.src_path}")
      add_app_module(
        workspace_dir_path=self.workspace_dir_path,
        app_module_path=event.src_path,
      )

  def on_deleted(self, event: FileSystemEvent):
    src_path = cast(str, event.src_path)
    if src_path.endswith(".py"):
      print(f"Stopped watching deleted Python module: {event.src_path}")
      remove_app_module(
        workspace_dir_path=self.workspace_dir_path,
        app_module_path=event.src_path,
      )


def fs_watcher(absolute_path: str):
  """
  Filesystem watcher using watchdog. Watches for any changes in the specified directory
  and triggers hot reload on change.
  """
  workspace_dir_path = os.path.dirname(absolute_path)
  # Initially track all the files on the file system and then rely on watchdog.
  for root, dirnames, files in os.walk(workspace_dir_path):
    # Filter out unusual directories, e.g. starting with "." because they
    # can be special directories, because venv directories
    # can have lots of Python files that are not application Python modules.
    new_dirnames: list[str] = []
    for d in dirnames:
      if d.startswith("."):
        continue
      if d == "__pycache__":
        continue
      if d == "venv":
        continue
      new_dirnames.append(d)

    dirnames[:] = new_dirnames

    for file in files:
      if file.endswith(".py"):
        full_path = os.path.join(root, file)
        relative_path = os.path.relpath(full_path, workspace_dir_path)
        add_app_module(
          workspace_dir_path=workspace_dir_path, app_module_path=relative_path
        )

  event_handler = ReloadEventHandler(
    absolute_path=absolute_path,
    workspace_dir_path=workspace_dir_path,
  )
  observer = Observer()
  observer.schedule(event_handler, path=workspace_dir_path, recursive=True)  # type: ignore
  observer.start()
  try:
    while True:
      time.sleep(0.1)
  except KeyboardInterrupt:
    observer.stop()
  observer.join()


def execute_main_module(absolute_path: str):
  try:
    # Clear app modules
    clear_app_modules()
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
