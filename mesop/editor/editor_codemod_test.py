import unittest

from libcst.codemod import (
  CodemodTest,
)

from mesop.editor.editor_codemod import ReplaceKeywordArg
from mesop.utils.runfiles import get_runfile_location


def load_testdata(filename: str) -> str:
  with open(
    get_runfile_location(f"mesop/mesop/editor/testdata/{filename}")
  ) as f:
    return f.read()


class TestReplaceKeywordArg(CodemodTest):
  TRANSFORM = ReplaceKeywordArg

  def test_replace(self) -> None:
    test_case_name = "simple_callsite"

    self.assertCodemod(
      load_testdata(f"{test_case_name}_before.py"),
      load_testdata(f"{test_case_name}_after.py"),
      fn_name="input",
      keyword_arg="label",
      arg_value="defa",
    )


if __name__ == "__main__":
  unittest.main()
