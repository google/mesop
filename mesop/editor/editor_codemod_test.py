import unittest

import libcst as cst
from libcst.codemod import (
  CodemodContext,
  CodemodTest,
  VisitorBasedCodemodCommand,
)


class ReplaceKeywordArg(VisitorBasedCodemodCommand):
  DESCRIPTION: str = "Converts keyword arg."

  def __init__(
    self,
    context: CodemodContext,
    fn_name: str,
    keyword_arg: str,
    arg_value: str,
  ) -> None:
    super().__init__(context)
    self.fn_name = fn_name
    self.keyword_arg = keyword_arg
    self.arg_value = arg_value

  def leave_Call(
    self, original_node: cst.Call, updated_node: cst.Call
  ) -> cst.BaseExpression:
    # Return original node if the function name doesn't match.
    if not (
      isinstance(updated_node.func, cst.Attribute)
      and updated_node.func.attr.value == self.fn_name
    ):
      return original_node

    new_args: list[cst.Arg] = []
    for arg in updated_node.args:
      if (
        isinstance(arg.keyword, cst.Name)
        and arg.keyword.value == self.keyword_arg
      ):
        # Replace the argument value
        new_arg = arg.with_changes(
          value=cst.SimpleString(f'"{self.arg_value}"')
        )
        new_args.append(new_arg)
      else:
        new_args.append(arg)
    return updated_node.with_changes(args=new_args)


class TestReplaceKeywordArg(CodemodTest):
  TRANSFORM = ReplaceKeywordArg

  def test_replace(self) -> None:
    before = """
            me.input(label="abc")
        """
    after = """
            me.input(label="defa")
        """

    # Verify the value is replaced
    self.assertCodemod(
      before, after, fn_name="input", keyword_arg="label", arg_value="defa"
    )


if __name__ == "__main__":
  unittest.main()
