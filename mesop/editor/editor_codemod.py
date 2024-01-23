"""Responsible for the code transformation logic. This exposes a simple API for doing
codemods to the rest of the Mesop editor package.
"""

from typing import Sequence

import libcst as cst
from libcst.codemod import (
  CodemodContext,
  SkipFile,
  VisitorBasedCodemodCommand,
)
from libcst.codemod.visitors import AddImportsVisitor
from libcst.metadata import CodeRange, PositionProvider

import mesop.protos.ui_pb2 as pb


class NewComponentCodemod(VisitorBasedCodemodCommand):
  DESCRIPTION: str = "Inserts new component callsite."
  METADATA_DEPENDENCIES = (PositionProvider,)

  def __init__(
    self, context: CodemodContext, input: pb.EditorNewComponent
  ) -> None:
    super().__init__(context)
    self.input = input
    component_name = self.input.component_name
    if component_name.HasField("module_path"):
      AddImportsVisitor.add_needed_import(
        self.context, component_name.module_path, component_name.fn_name
      )

  def leave_With(self, original_node: cst.With, updated_node: cst.With):
    position = self.get_metadata(PositionProvider, original_node)
    assert isinstance(position, CodeRange)
    if position.start.line != self.input.source_code_location.line:
      return updated_node
    if self.input.mode == pb.EditorNewComponent.Mode.MODE_APPEND_SIBLING:
      return cst.FlattenSentinel(
        [updated_node, create_component_callsite(self.input.component_name)]
      )

    updated_statement_lines: list[
      cst.BaseStatement | cst.BaseSmallStatement
    ] = []
    for statement in updated_node.body.body:
      # Copy everything except `pass`
      if not (
        isinstance(statement, cst.SimpleStatementLine)
        and len(statement.body) == 1
        and isinstance(statement.body[0], cst.Pass)
      ):
        updated_statement_lines.append(statement)

    if self.input.mode == pb.EditorNewComponent.Mode.MODE_CHILD:
      updated_statement_lines.append(
        create_component_callsite(self.input.component_name)
      )
    else:
      raise Exception("unsupported mode", self.input.mode)

    return updated_node.with_changes(
      body=updated_node.body.with_changes(body=updated_statement_lines)
    )

  def leave_SimpleStatementLine(
    self,
    original_node: cst.SimpleStatementLine,
    updated_node: cst.SimpleStatementLine,
  ):
    position = self.get_metadata(PositionProvider, original_node)
    assert isinstance(position, CodeRange)
    if position.start.line != self.input.source_code_location.line:
      return original_node
    if self.input.mode == pb.EditorNewComponent.Mode.MODE_APPEND_SIBLING:
      new_callsite = create_component_callsite(self.input.component_name)
      return cst.FlattenSentinel([updated_node, new_callsite])
    if self.input.mode == pb.EditorNewComponent.Mode.MODE_CHILD:
      assert len(original_node.body) == 1
      expr = original_node.body[0]
      assert isinstance(expr, cst.Expr)
      return cst.With(
        items=[cst.WithItem(item=expr.value)],
        body=cst.IndentedBlock(
          body=[create_component_callsite(self.input.component_name)]
        ),
      )
    raise Exception("Unsupported EditorNewComponent.Mode", self.input.mode)


class DeleteComponentCodemod(VisitorBasedCodemodCommand):
  DESCRIPTION: str = "Removes component callsite."
  METADATA_DEPENDENCIES = (PositionProvider,)

  def __init__(
    self, context: CodemodContext, input: pb.EditorDeleteComponent
  ) -> None:
    super().__init__(context)
    self.input = input

  def leave_SimpleStatementLine(
    self,
    original_node: cst.SimpleStatementLine,
    updated_node: cst.SimpleStatementLine,
  ):
    position = self.get_metadata(PositionProvider, original_node)
    assert isinstance(position, CodeRange)
    if position.start.line == self.input.source_code_location.line:
      # Delete the component callsite by replacing it with an empty statement
      return cst.SimpleStatementLine(body=[])
    return original_node


class UpdateCallsiteCodemod(VisitorBasedCodemodCommand):
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
      self.is_fn_component(updated_node.func, self.input.component_name)
      and position.start.line == self.input.source_code_location.line
    ):
      return updated_node

    component_name = self.input.component_name
    first_positional_arg = None
    if component_name.HasField("core_module") and component_name.fn_name in [
      "text",
      "markdown",
    ]:
      first_positional_arg = "text"
    if component_name.HasField("core_module") and component_name.fn_name in [
      "icon"
    ]:
      first_positional_arg = "icon"
    if component_name.fn_name in ["button"]:
      first_positional_arg = "label"
    return self._update_call(
      updated_node,
      self.input.arg_path.segments,
      first_positional_arg=first_positional_arg,
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
    new_value = self.get_value(self.input.replacement)
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
      arg_value = input_arg.value
      if not isinstance(arg_value, cst.Call):
        if not isinstance(arg_value, (cst.Integer, cst.SimpleString)) and not (
          isinstance(arg_value, cst.Name)
          and arg_value.value in ("True", "False", "None")  # handle None
        ):
          raise SkipFile("Skipping updating callsite because non-literal arg.")
        new_value = self.get_value(self.input.replacement)
        if new_value is None:
          return None
        mod = input_arg.with_changes(value=new_value)
        return mod
      call = arg_value

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
            elif self.input.replacement.HasField("delete_code"):
              # Make sure we want to delete the code; then skip this element.
              pass
            elif self.input.replacement.HasField("append_element"):
              # First, append the current element, and then add the new element.
              new_elements.append(element)
              new_elements.append(
                cst.Element(
                  value=self.get_code_value(
                    self.input.replacement.append_element
                  )
                )
              )
            else:
              raise Exception(
                "Unhandled replacement case", self.input.replacement
              )

          else:
            new_elements.append(element)

        return input_arg.with_changes(
          value=value.with_changes(elements=new_elements)
        )

      raise Exception("unexpected input_arg", input_arg)

  def is_fn_component(
    self, fn: cst.BaseExpression, component_name: pb.ComponentName
  ):
    if component_name.HasField("module_path"):
      if not isinstance(fn, cst.Name):
        return False
      return fn.value == component_name.fn_name
    if not isinstance(fn, cst.Attribute):
      return False
    if component_name.HasField("core_module"):
      if not isinstance(fn.value, cst.Name):
        return False
      if fn.value.value != get_module_name(self.input.component_name):
        return False
    if fn.attr.value != component_name.fn_name:
      return False
    return True

  def get_value(self, replacement: pb.CodeReplacement):
    if replacement.HasField("new_code"):
      return self.get_code_value(replacement.new_code)
    if replacement.HasField("delete_code"):
      return None
    if replacement.HasField("append_element"):
      return self.get_code_value(replacement.append_element)
    raise Exception("Unhandled replacement", replacement)

  def get_code_value(self, code: pb.CodeValue):
    if code.HasField("string_value"):
      string_value = code.string_value or "<new>"
      # Create multi-line string if needed.
      if "\n" in code.string_value:
        return cst.SimpleString(f'"""{string_value}"""')
      return cst.SimpleString(f'"{string_value}"')
    if code.HasField("double_value"):
      return cst.Float(str(code.double_value))
    if code.HasField("int_value"):
      return cst.Integer(str(code.int_value))
    if code.HasField("bool_value"):
      return cst.Name(str(code.bool_value))
    if code.HasField("struct_name"):
      return cst.Call(
        func=cst.Attribute(
          value=cst.Name(get_module_name(self.input.component_name)),
          attr=cst.Name(code.struct_name),
        )
      )
    raise Exception("Code value", code)


def create_component_callsite(component_name: pb.ComponentName):
  # module = component_name.module_path
  module_prefix = "me." if component_name.HasField("core_module") else ""
  return cst.parse_statement(f"{module_prefix}{component_name.fn_name}()")


def get_module_name(component_name: pb.ComponentName) -> str:
  if component_name.HasField("core_module"):
    return "me"
  return component_name.module_path
