from typing import Any, Callable

from pydantic import validate_arguments

import mesop.components.component_name.component_name_pb2 as component_name_pb
from mesop.component_helpers import handler_type, insert_component
from mesop.events import ClickEvent


@validate_arguments
def component_name(
  *,
  label: str,
  on_click: Callable[[Any, ClickEvent], Any] | None = None,
  key: str | None = None,
):
  """
  This function creates a component_name.

  Args:
      label (str): The text to be displayed
      on_click (Callable[..., Any]): The function to be called when the component is clicked.
  """
  insert_component(
    key=key,
    type_name="component_name",
    proto=component_name_pb.ComponentNameType(
      label=label,
      on_click_handler_id=handler_type(on_click),
    ),
  )
