from dataclasses import dataclass


class ClickEvent:
    pass


@dataclass
class CheckboxEvent:
    checked: bool
