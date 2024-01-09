import os

import mesop.protos.ui_pb2 as pb
from mesop.editor.editor_codemod import execute_codemod
from mesop.exceptions import MesopInternalException
from mesop.utils.path_utils import get_path_from_workspace_root


def handle_editor_event(event: pb.EditorEvent):
  print("Handling editor event", event)
  if event.HasField("update_callsite"):
    handle_update_callsite(event.update_callsite)
    return
  raise MesopInternalException("Not yet event implemented event", event)


def handle_update_callsite(update: pb.EditorUpdateCallsite):
  # Ignore the first part which is the Bazel workspace root (e.g. "mesop")
  module_segments = update.source_code_location.module.split(".")[1:]
  code_path = get_path_from_workspace_root(
    os.path.sep.join(module_segments) + ".py"
  )
  with open(code_path) as f:
    contents = f.read()

  with open(code_path, "w") as f:
    new_contents = execute_codemod(contents, update)
    f.write(new_contents)
    print("new_contents", new_contents)
