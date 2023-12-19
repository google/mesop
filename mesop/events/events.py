from dataclasses import dataclass


@dataclass
class MesopEvent:
  key: str


@dataclass
class ClickEvent(MesopEvent):
  pass


@dataclass
class InputEvent(MesopEvent):
  value: str


@dataclass
class ChangeEvent(MesopEvent):
  value: str
