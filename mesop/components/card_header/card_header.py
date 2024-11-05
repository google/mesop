from typing import Literal

import mesop.components.card_header.card_header_pb2 as card_header_pb
from mesop.component_helpers import insert_component, register_native_component


@register_native_component
def card_header(
  *,
  title: str,
  subtitle: str = "",
  image: str = "",
  image_type: Literal[
    "avatar", "small", "medium", "large", "extra-large"
  ] = "avatar",
  key: str | None = None,
):
  """
  This function creates a card_header.

  This component is meant to be used with the `card` component. It is used for the
  header of a card.

  This component is a optional. It is mainly used as a convenience for consistent
  formatting with the card component.

  Args:
      title: Title
      subtitle: Optional subtitle
      image: Optional image
      image_type: Display style for the image. Avatar will display as a circular image
          to the left of the title/subtitle. Small/medium/large/extra-large will display
          a right-aligned image of the specified size.
  """
  insert_component(
    key=key,
    type_name="card_header",
    proto=card_header_pb.CardHeaderType(
      title=title,
      subtitle=subtitle,
      image=image,
      image_type=image_type,
    ),
  )
