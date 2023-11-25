from dataclasses import dataclass
from optic.key import Key


class ClickEvent:
    key: Key


@dataclass
class CheckboxEvent:
    key: Key
    checked: bool


@dataclass
class ChangeEvent:
    key: Key
    value: str
