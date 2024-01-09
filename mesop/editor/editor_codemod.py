"""Responsible for the code transformation logic. This exposes a simple API for doing
codemods to the rest of the Mesop editor package.
"""

import libcst as cst
from libcst.codemod import (
  CodemodContext,
  VisitorBasedCodemodCommand,
)
from libcst.metadata import CodeRange, PositionProvider

import mesop.protos.ui_pb2 as pb


def execute_codemod(source_code: str, input: pb.EditorUpdateCallsite) -> str:
  context = CodemodContext()
  tree = cst.parse_module(source_code)

  codemod = ReplaceKeywordArg(context, input)

  modified_tree = codemod.transform_module(tree)

  return modified_tree.code


class ReplaceKeywordArg(VisitorBasedCodemodCommand):
  DESCRIPTION: str = "Converts keyword arg."
  METADATA_DEPENDENCIES = (PositionProvider,)

  def __init__(
    self, context: CodemodContext, input: pb.EditorUpdateCallsite
  ) -> None:
    super().__init__(context)
    self.input = input

  def leave_Call(
    self, original_node: cst.Call, updated_node: cst.Call
  ) -> cst.BaseExpression:
    position = self.get_metadata(PositionProvider, original_node)
    assert isinstance(position, CodeRange)

    # Return original node if the function name doesn't match.
    if not (
      isinstance(updated_node.func, cst.Attribute)
      and updated_node.func.attr.value == self.input.component_name
      and position.start.line == self.input.source_code_location.line
    ):
      return original_node

    new_args: list[cst.Arg] = []
    for arg in updated_node.args:
      if (
        isinstance(arg.keyword, cst.Name)
        and arg.keyword.value == self.input.keyword_argument
      ) or (
        self.input.component_name in ["text", "markdown"]
        and self.input.keyword_argument == "text"
        and arg == updated_node.args[0]
      ):
        # Replace the argument value
        new_arg = arg.with_changes(
          value=cst.SimpleString(f'"{self.input.new_code}"')
        )
        new_args.append(new_arg)
      else:
        new_args.append(arg)
    return updated_node.with_changes(args=new_args)
