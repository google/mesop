from mesop.component_helpers import Style
from mesop.components.box.box import box


def columns(columns: int = 2):
  return box(style=Style(columns=columns))
