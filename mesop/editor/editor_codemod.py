"""Responsible for the code transformation logic. This exposes a simple API for doing
codemods to the rest of the Mesop editor package.
"""

from typing import Sequence

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

    return self._update_call(
      updated_node,
      self.input.arg_path.segments,
      first_positional_arg=(
        "text" if self.input.component_name in ["text", "markdown"] else None
      ),
    )

  def _update_call(
    self,
    call: cst.Call,
    segments: Sequence[pb.ArgPathSegment],
    first_positional_arg: str | None = None,
  ) -> cst.Call:
    segment = segments[0]
    keyword_argument = segment.keyword_argument
    new_args: list[cst.Arg] = []
    found_arg = False
    for arg in call.args:
      if (
        isinstance(arg.keyword, cst.Name)
        and arg.keyword.value == keyword_argument
      ) or (
        first_positional_arg is not None
        and keyword_argument == first_positional_arg
        and arg == call.args[0]
      ):
        found_arg = True
        new_args.append(self.modify_arg(arg, segments))
      else:
        new_args.append(arg)
    if not found_arg:
      new_args.append(
        cst.Arg(
          keyword=cst.Name(segment.keyword_argument),
          value=get_value(self.input.new_code),
        )
      )
    return call.with_changes(args=new_args)

  def modify_arg(
    self, input_arg: cst.Arg, segments: Sequence[pb.ArgPathSegment]
  ) -> cst.Arg:
    if len(segments) == 1:
      maybe_call = input_arg.value
      if not isinstance(maybe_call, cst.Call):
        mod = input_arg.with_changes(value=get_value(self.input.new_code))
        return mod
      call = maybe_call
      return input_arg.with_changes(value=self._update_call(call, segments))
    else:
      call = input_arg.value
      if not isinstance(call, cst.Call):
        raise Exception("unexpected input_arg", input_arg)

      return input_arg.with_changes(value=self._update_call(call, segments[1:]))


def get_value(code: pb.CodeValue):
  if code.HasField("string_value"):
    # Create multi-line string if needed.
    if "\n" in code.string_value:
      return cst.SimpleString(f'"""{code.string_value}"""')
    return cst.SimpleString(f'"{code.string_value}"')
  if code.HasField("double_value"):
    return cst.Float(str(code.double_value))
  if code.HasField("int_value"):
    return cst.Integer(str(code.int_value))
  if code.HasField("bool_value"):
    return cst.Name(str(code.bool_value))
  if code.HasField("struct_name"):
    return cst.Call(
      func=cst.Attribute(value=cst.Name("me"), attr=cst.Name(code.struct_name))
    )
  raise Exception("Code value", code)
