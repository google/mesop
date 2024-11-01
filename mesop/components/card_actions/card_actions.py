from typing import Literal

import mesop.components.card_actions.card_actions_pb2 as card_actions_pb
from mesop.component_helpers import (
  insert_composite_component,
  register_native_component,
)


@register_native_component
def card_actions(
  *,
  align: Literal["start", "end"],
  key: str | None = None,
):
  """
  This function creates a card_actions.

  This component is meant to be used with the `card` component. It is used for the
  bottom area of a card that contains action buttons.

  This component is a optional. It is mainly used as a convenience for consistent
  formatting with the card component.

  Args:
      align: Align elements to the left (start) or right (end).
  """
  return insert_composite_component(
    key=key,
    type_name="card_actions",
    proto=card_actions_pb.CardActionsType(
      align=align,
    ),
  )
