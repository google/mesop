from dataclasses import dataclass


@dataclass(kw_only=True)
class MesopEvent:
  key: str


@dataclass(kw_only=True)
class ClickEvent(MesopEvent):
  """Represents a user click event.

  Attributes:
      key (str): key of the component that emitted this event.
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
