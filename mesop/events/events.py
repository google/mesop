from dataclasses import dataclass


@dataclass
class MesopEvent:
  key: str


@dataclass
class ClickEvent(MesopEvent):
  """Represents a user click event.

  Attributes:
      key (str): key of the component that emitted this event.
  """

  pass


@dataclass
class InputEvent(MesopEvent):
  """Represents a user input event.

  Attributes:
      value: Input value.
      key (str): key of the component that emitted this event.
  """

  value: str
