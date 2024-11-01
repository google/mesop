from typing import Literal

import mesop.components.card.card_pb2 as card_pb
from mesop.component_helpers import (
  Style,
  insert_composite_component,
  register_native_component,
)


@register_native_component
def card(
  *,
  appearance: Literal["outlined", "raised"] = "outlined",
  style: Style | None = None,
  key: str | None = None,
):
  """
  This function creates a card.

  Args:
      appearance: Card appearance style: outlined or raised.
      style: Style for the component.
      key: The component [key](../components/index.md#component-key).
  """
  return insert_composite_component(
    key=key,
    type_name="card",
    style=style,
    proto=card_pb.CardType(
      appearance=appearance,
    ),
  )
