from pydantic import validate_arguments

import mesop.components.text.text_pb2 as text_pb2
from mesop.component_helpers import insert_component


@validate_arguments
def text(
  *,
  text: str,
  key: str | None = None,
):
  insert_component(
    key=key, type_name="text", proto=text_pb2.TextType(text=text)
  )
