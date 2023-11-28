from pydantic import validate_arguments

from typing import Any, Callable
import protos.ui_pb2 as pb
import optic.components.component_name.component_name_pb2 as component_name_pb
from optic.component_helpers import insert_component, handler_type
from optic.events import ClickEvent


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
        type=pb.Type(
            name="component_name",
            value=component_name_pb.ComponentNameType(
                label=label,
                on_click_handler_id=handler_type(on_click) if on_click else None,
            ).SerializeToString(),
        ),
    )
