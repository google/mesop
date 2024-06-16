from typing import Literal

import mesop.components.badge.badge_pb2 as badge_pb
from mesop.component_helpers import (
  insert_composite_component,
  register_native_component,
)


@register_native_component
def badge(
  *,
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
  key: str | None = None,
):
  """Creates a Badge component.
  Badge is a composite component.

  Args:
    color: The color of the badge. Can be `primary`, `accent`, or `warn`.
    overlap: Whether the badge should overlap its contents or not
    disabled: Whether the badge is disabled.
    position: Position the badge should reside. Accepts any combination of 'above'|'below' and 'before'|'after'
    content: The content for the badge
    description: Message used to describe the decorated element via aria-describedby
    size: Size of the badge. Can be 'small', 'medium', or 'large'.
    hidden: Whether the badge is hidden.
    key: The component [key](../components/index.md#component-key).
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
    ),
  )
