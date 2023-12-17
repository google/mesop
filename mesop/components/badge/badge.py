from typing import Literal

from pydantic import validate_arguments

import mesop.components.badge.badge_pb2 as badge_pb
from mesop.component_helpers import (
  insert_composite_component,
)


@validate_arguments
def badge(
  *,
  key: str | None = None,
  color: Literal["primary", "accent", "warn"] = "primary",
  overlap: bool = False,
  disabled: bool = False,
  position: Literal[
    "above after",
    "above before",
    "below before",
    "below after",
    "before",
    "after",
    "above",
    "below",
  ] = "above after",
  content: str = "",
  description: str = "",
  size: Literal["small", "medium", "large"] = "small",
  hidden: bool = False,
  variant: Literal["matBadge"] = "matBadge",
):
  """Creates a Badge component.
  Badge is a composite component.

  Args:
    key (str|None): Unique identifier for this component instance.
    color (Literal['primary','accent','warn']): The color of the badge. Can be `primary`, `accent`, or `warn`.
    overlap (bool): Whether the badge should overlap its contents or not
    disabled (bool): Whether the badge is disabled.
    position (Literal['above after','above before','below before','below after','before','after','above','below']): Position the badge should reside. Accepts any combination of 'above'|'below' and 'before'|'after'
    content (str): The content for the badge
    description (str): Message used to describe the decorated element via aria-describedby
    size (Literal['small','medium','large']): Size of the badge. Can be 'small', 'medium', or 'large'.
    hidden (bool): Whether the badge is hidden.
    variant (Literal['matBadge']): component variations
  """
  return insert_composite_component(
    key=key,
    type_name="badge",
    proto=badge_pb.BadgeType(
      color=color,
      overlap=overlap,
      disabled=disabled,
      position=position,
      content=content,
      description=description,
      size=size,
      hidden=hidden,
      variant_index=_get_variant_index(variant),
    ),
  )


def _get_variant_index(variant: str) -> int:
  if variant == "matBadge":
    return 0
  raise Exception("Unexpected variant: " + variant)
