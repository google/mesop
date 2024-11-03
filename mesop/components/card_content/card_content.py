import mesop.components.card_content.card_content_pb2 as card_content_pb
from mesop.component_helpers import (
  insert_composite_component,
  register_native_component,
)


@register_native_component
def card_content(
  *,
  key: str | None = None,
):
  """
  This function creates a card_content.

  This component is meant to be used with the `card` component. It is used for the
  contents of a card that

  This component is a optional. It is mainly used as a convenience for consistent
  formatting with the card component.
  """
  return insert_composite_component(
    key=key,
    type_name="card_content",
    proto=card_content_pb.CardContentType(),
  )
