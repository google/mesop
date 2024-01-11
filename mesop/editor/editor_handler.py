import os

import libcst as cst
from libcst.codemod import (
  CodemodContext,
  VisitorBasedCodemodCommand,
)

import mesop.protos.ui_pb2 as pb
from mesop.editor.editor_codemod import (
  DeleteComponentCodemod,
  NewComponentCodemod,
  UpdateCallsiteCodemod,
)
from mesop.exceptions import MesopInternalException
from mesop.utils.path_utils import get_path_from_workspace_root


def handle_editor_event(event: pb.EditorEvent):
  print("Handling editor event", event)
  if event.HasField("update_callsite"):
    run_codemod(
      event.update_callsite.source_code_location,
      UpdateCallsiteCodemod(CodemodContext(), event.update_callsite),
    )
    return
  if event.HasField("new_component"):
    run_codemod(
      event.new_component.source_code_location,
      NewComponentCodemod(CodemodContext(), event.new_component),
    )
    return
  if event.HasField("delete_component"):
    run_codemod(
      event.delete_component.source_code_location,
      DeleteComponentCodemod(CodemodContext(), event.delete_component),
    )
    return
  raise MesopInternalException("Not yet event implemented event", event)


def run_codemod(
  location: pb.SourceCodeLocation, codemod: VisitorBasedCodemodCommand
):
  # Ignore the first part which is the Bazel workspace root (e.g. "mesop")
  module_segments = location.module.split(".")[1:]
  code_path = get_path_from_workspace_root(
    os.path.sep.join(module_segments) + ".py"
  )
  with open(code_path) as f:
    source_code = f.read()

  tree = cst.parse_module(source_code)
  modified_tree = codemod.transform_module(tree)
  new_source_code = modified_tree.code

  with open(code_path, "w") as f:
    f.write(new_source_code)
