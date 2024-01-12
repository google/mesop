from mesop.component_helpers import Style, component
from mesop.components.box.box import box


@component
def columns(columns: int = 2):
  return box(style=Style(columns=columns))
