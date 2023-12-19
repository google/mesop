from pydantic import validate_arguments

import mesop.components.markdown.markdown_pb2 as markdown_pb
from mesop.component_helpers import insert_component


@validate_arguments
def markdown(
  text: str,
  *,
  key: str | None = None,
):
  """
  This function creates a markdown.

  Args:
      text: Markdown text
  """
  insert_component(
    key=key,
    type_name="markdown",
    proto=markdown_pb.MarkdownType(
      text=text,
    ),
  )
