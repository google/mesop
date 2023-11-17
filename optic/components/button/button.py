from pydantic import validate_arguments

from typing import Any, Callable
import protos.ui_pb2 as pb
import optic.components.button.button_pb2 as button_pb
from optic.component_helpers import insert_component, handler_type
from optic.state.events import ClickEvent


@validate_arguments
def button(
    *,
    label: str,
    on_click: Callable[[Any, ClickEvent], Any],
    key: str | None = None,
):
    """
    This function creates a button component with a label and an on_click event.

    Args:
        label (str): The text to be displayed on the button.
        on_click (Callable[..., Any]): The function to be called when the button is clicked.
    """
    insert_component(
        key=key,
        type=pb.Type(
            name="button",
            value=button_pb.ButtonType(
                label=label,
                on_click_handler_id=handler_type(on_click),
            ).SerializeToString(),
        ),
    )
