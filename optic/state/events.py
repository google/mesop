from dataclasses import dataclass
from .key import Key


class ClickEvent:
    key: Key


@dataclass
class CheckboxEvent:
    key: Key
    checked: bool
