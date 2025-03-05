from typing import Any, Callable

import mesop as me
import mesop.labs as mel


@me.slotclass
class LayoutSlots:
  header: me.NamedSlot
  footer: me.NamedSlot


@mel.web_component(path="./outer_component.js")
def outer_component(
  *,
  value: int,
  on_increment: Callable[[mel.WebEvent], Any],
  key: str | None = None,
):
  return mel.insert_web_component(
    name="slot-outer-component",
    key=key,
    events={
      "incrementEvent": on_increment,
    },
    properties={
      "value": value,
      "active": True,
    },
    named_slots=LayoutSlots,
  )
