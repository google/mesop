import unittest

from libcst.codemod import (
  CodemodTest,
)

import mesop.protos.ui_pb2 as pb
from mesop.editor.editor_codemod import ReplaceKeywordArg
from mesop.utils.runfiles import get_runfile_location


def load_testdata(dir: str, filename: str) -> str:
  with open(
    get_runfile_location(f"mesop/mesop/editor/testdata/{dir}/{filename}")
  ) as f:
    return f.read()


class TestReplaceKeywordArg(CodemodTest):
  TRANSFORM = ReplaceKeywordArg

  def test_simple_callsite(self) -> None:
    self.assertEditorUpdate(
      "simple_callsite",
      pb.EditorUpdateCallsite(
        component_name="input",
        arg_path=pb.ArgPath(
          segments=[pb.ArgPathSegment(keyword_argument="label")]
        ),
        new_code="defa",
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
        new_code="defa",
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
        new_code="after",
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
        new_code="after",
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
        new_code="pink",
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
