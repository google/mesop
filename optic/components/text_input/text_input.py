from pydantic import validate_arguments

from typing import Any, Callable
import protos.ui_pb2 as pb
import optic.components.text_input.text_input_pb2 as text_input_pb
from optic.component_helpers import insert_component, handler_type
from optic.events import ClickEvent


@validate_arguments
def text_input(
    *,
    label: str,
    on_click: Callable[[Any, ClickEvent], Any],
    key: str | None = None,
):
    """
    This function creates a text_input.

    Args:
        label (str): The text to be displayed
        on_click (Callable[..., Any]): The function to be called when the component is clicked.
    """
    insert_component(
        key=key,
        type=pb.Type(
            name="text_input",
            value=text_input_pb.TextInputType(
                label=label,
                on_click_handler_id=handler_type(on_click),
            ).SerializeToString(),
        ),
    )
