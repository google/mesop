from dataclasses import dataclass

from mesop.key import Key


@dataclass
class MesopEvent:
  key: Key


@dataclass
class ClickEvent(MesopEvent):
  pass


@dataclass
class ChangeEvent(MesopEvent):
  value: str
