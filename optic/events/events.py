from dataclasses import dataclass

from optic.key import Key


@dataclass
class OpticEvent:
  key: Key


@dataclass
class ClickEvent(OpticEvent):
  pass


@dataclass
class ChangeEvent(OpticEvent):
  value: str
