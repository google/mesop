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

  def leave_Call(  # type: ignore (erroneously forbids return type with `None`)
    self, original_node: cst.Call, updated_node: cst.Call
  ) -> cst.BaseExpression | None:
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
        new_arg = self.modify_arg(arg, segments)
        if new_arg:
          new_args.append(new_arg)
      else:
        new_args.append(arg)
    new_value = get_value(self.input.replacement)
    if not found_arg and new_value:
      if not segment.keyword_argument:
        raise Exception("Did not receive keyword_argument", segments, call)
      new_args.append(
        cst.Arg(
          keyword=cst.Name(segment.keyword_argument),
          value=new_value,
        )
      )
    return call.with_changes(args=new_args)

  def modify_arg(
    self, input_arg: cst.Arg, segments: Sequence[pb.ArgPathSegment]
  ) -> cst.Arg | None:
    if len(segments) == 1:
      maybe_call = input_arg.value
      if not isinstance(maybe_call, cst.Call):
        new_value = get_value(self.input.replacement)
        if new_value is None:
          return None
        mod = input_arg.with_changes(value=new_value)
        return mod
      call = maybe_call

      if (
        input_arg.keyword
        and input_arg.keyword.value == segments[0].keyword_argument
        and self.input.replacement.HasField("delete_code")
      ):
        return None
      return input_arg.with_changes(value=self._update_call(call, segments))
    else:
      value = input_arg.value
      if isinstance(value, cst.Call):
        return input_arg.with_changes(
          value=self._update_call(value, segments[1:])
        )
      if isinstance(value, cst.List):
        list_value = value
        # In the example of Radio's options:
        # segments[0] = "options"
        # segments[1] = list_index
        if not segments[1].HasField("list_index"):
          raise Exception(
            "Expected to have a list index at segments[1] of ",
            segments,
            input_arg,
          )
        new_elements: list[cst.BaseElement] = []
        for i, element in enumerate(list_value.elements):
          if i == segments[1].list_index:
            element = list_value.elements[segments[1].list_index]
            assert isinstance(element.value, cst.Call)
            if segments[2:]:
              new_elements.append(
                element.with_changes(
                  value=self._update_call(element.value, segments[2:])
                )
              )
            else:
              # Make sure we want to delete the code; then skip this element.
              assert self.input.replacement.HasField("delete_code")

          else:
            new_elements.append(element)

        return input_arg.with_changes(
          value=value.with_changes(elements=new_elements)
        )

      raise Exception("unexpected input_arg", input_arg)


def get_value(replacement: pb.CodeReplacement):
  if replacement.HasField("new_code"):
    return get_code_value(replacement.new_code)
  if replacement.HasField("delete_code"):
    return None
  raise Exception("Unhandled replacement", replacement)


def get_code_value(code: pb.CodeValue):
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
