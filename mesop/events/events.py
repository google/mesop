from dataclasses import dataclass
from typing import Any


@dataclass(kw_only=True)
class MesopEvent:
  key: str


@dataclass(kw_only=True)
class ClickEvent(MesopEvent):
  """Represents a user click event.

  Attributes:
      key (str): key of the component that emitted this event.
      is_target: Whether the clicked target is the component which attached the event handler.
      client_x: X coordinate relative to the viewport.
      client_y: Y coordinate relative to the viewport.
      page_x: X coordinate relative to the entire document, including scrolled parts.
      page_y: Y coordinate relative to the entire document, including scrolled parts.
      offset_x: X coordinate relative to the element.
      offset_y: Y coordinate relative to the element.
  """

  is_target: bool
  client_x: float
  client_y: float
  page_x: float
  page_y: float
  offset_x: float
  offset_y: float


@dataclass(kw_only=True)
class RightClickEvent(ClickEvent):
  """Represents a user right click event.

  Attributes:
      key (str): key of the component that emitted this event.
      is_target (bool): Whether the clicked target is the component which attached the event handler.
      client_x (float): X coordinate relative to the viewport
      client_y (float): Y coordinate relative to the viewport
      page_x (float): X coordinate relative to the entire document, including scrolled parts
      page_y (float): Y coordinate relative to the entire document, including scrolled parts
      offset_x (float): X coordinate relative to the element
      offset_y (float): Y coordinate relative to the element
  """

  pass


@dataclass(kw_only=True)
class InputEvent(MesopEvent):
  """Represents a user input event.

  Attributes:
      value: Input value.
      key (str): key of the component that emitted this event.
  """

  value: str


# Note: LoadEvent intentionally does not inherit from MesopEvent
# because it doesn't originate from a component, thus a key
# does not apply.


@dataclass(kw_only=True)
class LoadEvent:
  """Represents a page load event.

  Attributes:
      path: The path loaded
  """

  path: str


@dataclass(kw_only=True)
class WebEvent(MesopEvent):
  """An event emitted by a web component.

  Attributes:
      value: The value associated with the web event.
      key (str): key of the component that emitted this event.
  """

  value: Any
