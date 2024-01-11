import unittest

from libcst.codemod import (
  CodemodTest,
)

import mesop.protos.ui_pb2 as pb
from mesop.editor.editor_codemod import (
  DeleteComponentCodemod,
  NewComponentCodemod,
  UpdateCallsiteCodemod,
)
from mesop.utils.runfiles import get_runfile_location


def load_testdata(dir: str, filename: str) -> str:
  with open(
    get_runfile_location(f"mesop/mesop/editor/testdata/{dir}/{filename}")
  ) as f:
    return f.read()


class TestDeleteComponentCodemod(CodemodTest):
  TRANSFORM = DeleteComponentCodemod

  def test_delete_component(self) -> None:
    self.assertEditorUpdate(
      "delete_component",
      pb.EditorDeleteComponent(
        source_code_location=pb.SourceCodeLocation(line=6),
      ),
    )

  def test_delete_only_component(self) -> None:
    self.assertEditorUpdate(
      "delete_only_component",
      pb.EditorDeleteComponent(
        source_code_location=pb.SourceCodeLocation(line=5),
      ),
    )

  def assertEditorUpdate(
    self, test_case_name: str, input: pb.EditorDeleteComponent
  ):
    self.assertCodemod(
      load_testdata(dir=test_case_name, filename="before.py"),
      load_testdata(dir=test_case_name, filename="after.py"),
      input=input,
    )


class TestNewComponentCodemod(CodemodTest):
  TRANSFORM = NewComponentCodemod

  def test_new_component(self) -> None:
    self.assertEditorUpdate(
      "new_component",
      pb.EditorNewComponent(
        component_name="divider",
        source_code_location=pb.SourceCodeLocation(line=5),
        mode=pb.EditorNewComponent.Mode.MODE_APPEND_SIBLING,
      ),
    )

  def test_new_component_nested_sibling(self) -> None:
    self.assertEditorUpdate(
      "new_component_nested_sibling",
      pb.EditorNewComponent(
        component_name="divider",
        source_code_location=pb.SourceCodeLocation(line=6),
        mode=pb.EditorNewComponent.Mode.MODE_APPEND_SIBLING,
      ),
    )

  def test_new_component_child(self) -> None:
    self.assertEditorUpdate(
      "new_component_child",
      pb.EditorNewComponent(
        component_name="text",
        source_code_location=pb.SourceCodeLocation(line=5),
        mode=pb.EditorNewComponent.Mode.MODE_CHILD,
      ),
    )

  def test_new_component_child_existing_with(self) -> None:
    self.assertEditorUpdate(
      "new_component_child_existing_with",
      pb.EditorNewComponent(
        component_name="text",
        source_code_location=pb.SourceCodeLocation(line=5),
        mode=pb.EditorNewComponent.Mode.MODE_CHILD,
      ),
    )

  def test_new_component_child_existing_with_pass(self) -> None:
    self.assertEditorUpdate(
      "new_component_child_existing_with_pass",
      pb.EditorNewComponent(
        component_name="text",
        source_code_location=pb.SourceCodeLocation(line=5),
        mode=pb.EditorNewComponent.Mode.MODE_CHILD,
      ),
    )

  def assertEditorUpdate(
    self, test_case_name: str, input: pb.EditorNewComponent
  ):
    self.assertCodemod(
      load_testdata(dir=test_case_name, filename="before.py"),
      load_testdata(dir=test_case_name, filename="after.py"),
      input=input,
    )


class TestUpdateCallsiteCodemod(CodemodTest):
  TRANSFORM = UpdateCallsiteCodemod

  def test_simple_callsite(self) -> None:
    self.assertEditorUpdate(
      "simple_callsite",
      pb.EditorUpdateCallsite(
        component_name="input",
        arg_path=pb.ArgPath(
          segments=[pb.ArgPathSegment(keyword_argument="label")]
        ),
        replacement=pb.CodeReplacement(
          new_code=pb.CodeValue(string_value="defa"),
        ),
        source_code_location=pb.SourceCodeLocation(line=5),
      ),
    )

  def test_multi_callsite(self) -> None:
    self.assertEditorUpdate(
      "multi_callsite",
      pb.EditorUpdateCallsite(
        component_name="input",
        arg_path=pb.ArgPath(
          segments=[pb.ArgPathSegment(keyword_argument="label")]
        ),
        replacement=pb.CodeReplacement(
          new_code=pb.CodeValue(string_value="defa"),
        ),
        source_code_location=pb.SourceCodeLocation(line=6),
      ),
    )

  def test_text(self) -> None:
    self.assertEditorUpdate(
      "text",
      pb.EditorUpdateCallsite(
        component_name="text",
        arg_path=pb.ArgPath(
          segments=[pb.ArgPathSegment(keyword_argument="text")]
        ),
        replacement=pb.CodeReplacement(
          new_code=pb.CodeValue(string_value="after"),
        ),
        source_code_location=pb.SourceCodeLocation(line=5),
      ),
    )

  def test_markdown(self) -> None:
    self.assertEditorUpdate(
      "markdown",
      pb.EditorUpdateCallsite(
        component_name="markdown",
        arg_path=pb.ArgPath(
          segments=[pb.ArgPathSegment(keyword_argument="text")]
        ),
        replacement=pb.CodeReplacement(
          new_code=pb.CodeValue(string_value="after"),
        ),
        source_code_location=pb.SourceCodeLocation(line=5),
      ),
    )

  def test_style_struct(self) -> None:
    self.assertEditorUpdate(
      "style_struct",
      pb.EditorUpdateCallsite(
        component_name="box",
        arg_path=pb.ArgPath(
          segments=[
            pb.ArgPathSegment(keyword_argument="style"),
            pb.ArgPathSegment(keyword_argument="background"),
          ]
        ),
        replacement=pb.CodeReplacement(
          new_code=pb.CodeValue(string_value="pink"),
        ),
        source_code_location=pb.SourceCodeLocation(line=5),
      ),
    )

  def test_style_nested_struct(self) -> None:
    self.assertEditorUpdate(
      "style_nested_struct",
      pb.EditorUpdateCallsite(
        component_name="box",
        arg_path=pb.ArgPath(
          segments=[
            pb.ArgPathSegment(keyword_argument="style"),
            pb.ArgPathSegment(keyword_argument="margin"),
            pb.ArgPathSegment(keyword_argument="top"),
          ]
        ),
        replacement=pb.CodeReplacement(
          new_code=pb.CodeValue(int_value=8),
        ),
        source_code_location=pb.SourceCodeLocation(line=5),
      ),
    )

  def test_bool(self) -> None:
    self.assertEditorUpdate(
      "bool",
      pb.EditorUpdateCallsite(
        component_name="checkbox",
        arg_path=pb.ArgPath(
          segments=[
            pb.ArgPathSegment(keyword_argument="checked"),
          ]
        ),
        replacement=pb.CodeReplacement(
          new_code=pb.CodeValue(bool_value=False),
        ),
        source_code_location=pb.SourceCodeLocation(line=5),
      ),
    )

  def test_input_add_property(self) -> None:
    self.assertEditorUpdate(
      "input_add_property",
      pb.EditorUpdateCallsite(
        component_name="input",
        arg_path=pb.ArgPath(
          segments=[
            pb.ArgPathSegment(keyword_argument="label"),
          ]
        ),
        replacement=pb.CodeReplacement(
          new_code=pb.CodeValue(string_value="foo"),
        ),
        source_code_location=pb.SourceCodeLocation(line=5),
      ),
    )

  def test_input_add_complex_property(self) -> None:
    self.assertEditorUpdate(
      "input_add_complex_property",
      pb.EditorUpdateCallsite(
        component_name="input",
        arg_path=pb.ArgPath(
          segments=[
            pb.ArgPathSegment(keyword_argument="style"),
            pb.ArgPathSegment(keyword_argument="padding"),
          ]
        ),
        replacement=pb.CodeReplacement(
          new_code=pb.CodeValue(struct_name="Padding"),
        ),
        source_code_location=pb.SourceCodeLocation(line=5),
      ),
    )

  def test_list_append_element(self) -> None:
    self.assertEditorUpdate(
      "list_append_element",
      pb.EditorUpdateCallsite(
        component_name="radio",
        arg_path=pb.ArgPath(
          segments=[
            pb.ArgPathSegment(keyword_argument="options"),
            pb.ArgPathSegment(list_index=1),
          ]
        ),
        replacement=pb.CodeReplacement(
          append_element=pb.CodeValue(struct_name="RadioOption")
        ),
        source_code_location=pb.SourceCodeLocation(line=5),
      ),
    )

  def test_list_delete_element(self) -> None:
    self.assertEditorUpdate(
      "list_delete_element",
      pb.EditorUpdateCallsite(
        component_name="radio",
        arg_path=pb.ArgPath(
          segments=[
            pb.ArgPathSegment(keyword_argument="options"),
            pb.ArgPathSegment(list_index=0),
          ]
        ),
        replacement=pb.CodeReplacement(delete_code=pb.DeleteCode()),
        source_code_location=pb.SourceCodeLocation(line=5),
      ),
    )

  def test_list_edit_element(self) -> None:
    self.assertEditorUpdate(
      "list_edit_element",
      pb.EditorUpdateCallsite(
        component_name="radio",
        arg_path=pb.ArgPath(
          segments=[
            pb.ArgPathSegment(keyword_argument="options"),
            pb.ArgPathSegment(list_index=1),
            pb.ArgPathSegment(keyword_argument="label"),
          ]
        ),
        replacement=pb.CodeReplacement(
          new_code=pb.CodeValue(string_value="edited"),
        ),
        source_code_location=pb.SourceCodeLocation(line=5),
      ),
    )

  def test_delete_keyword_arg(self) -> None:
    self.assertEditorUpdate(
      "delete_keyword_arg",
      pb.EditorUpdateCallsite(
        component_name="input",
        arg_path=pb.ArgPath(
          segments=[
            pb.ArgPathSegment(keyword_argument="label"),
          ]
        ),
        replacement=pb.CodeReplacement(
          delete_code=pb.DeleteCode(),
        ),
        source_code_location=pb.SourceCodeLocation(line=5),
      ),
    )

  def test_delete_key(self) -> None:
    self.assertEditorUpdate(
      "delete_key",
      pb.EditorUpdateCallsite(
        component_name="input",
        arg_path=pb.ArgPath(
          segments=[
            pb.ArgPathSegment(keyword_argument="key"),
          ]
        ),
        replacement=pb.CodeReplacement(
          delete_code=pb.DeleteCode(),
        ),
        source_code_location=pb.SourceCodeLocation(line=5),
      ),
    )

  def test_delete_struct(self) -> None:
    self.assertEditorUpdate(
      "delete_struct",
      pb.EditorUpdateCallsite(
        component_name="input",
        arg_path=pb.ArgPath(
          segments=[
            pb.ArgPathSegment(keyword_argument="style"),
          ]
        ),
        replacement=pb.CodeReplacement(
          delete_code=pb.DeleteCode(),
        ),
        source_code_location=pb.SourceCodeLocation(line=5),
      ),
    )

  def test_multiline_string(self) -> None:
    self.assertEditorUpdate(
      "multiline_string",
      pb.EditorUpdateCallsite(
        component_name="markdown",
        arg_path=pb.ArgPath(
          segments=[
            pb.ArgPathSegment(keyword_argument="text"),
          ]
        ),
        replacement=pb.CodeReplacement(
          new_code=pb.CodeValue(
            string_value="""Welcome

    1 more line.
    Add 1 more line."""
          )
        ),
        source_code_location=pb.SourceCodeLocation(line=5),
      ),
    )

  def assertEditorUpdate(
    self, test_case_name: str, input: pb.EditorUpdateCallsite
  ):
    self.assertCodemod(
      load_testdata(dir=test_case_name, filename="before.py"),
      load_testdata(dir=test_case_name, filename="after.py"),
      input=input,
    )


if __name__ == "__main__":
  unittest.main()
