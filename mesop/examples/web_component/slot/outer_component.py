from typing import Any, Callable

import mesop.labs as mel

# Intentionally use mesop.labs to make sure
# we don't break apps using the pre-v1 web component API namespace.


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
  )
