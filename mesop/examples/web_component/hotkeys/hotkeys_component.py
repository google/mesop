from dataclasses import asdict, dataclass, field
from typing import Any, Callable, Literal

import mesop.labs as mel


@dataclass
class HotKey:
  key: str
  action: str
  modifiers: list[Literal["ctrl", "alt", "shift", "meta"]] = field(
    default_factory=list
  )


@mel.web_component(path="./hotkeys_component.js")
def hotkeys_component(
  *,
  hotkeys: list[HotKey],
  on_hotkey_press: Callable[[mel.WebEvent], Any],
  key: str | None = None,
):
  return mel.insert_web_component(
    name="hotkeys-component",
    key=key,
    events={
      "keyPressEvent": on_hotkey_press,
    },
    # Unable to serialize dataclass, so converting to dict.
    properties={"hotkeys": [asdict(hotkey) for hotkey in hotkeys]},
  )
