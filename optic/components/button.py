from typing import Any, Callable
import protos.ui_pb2 as pb
from optic.components.helper import insert_component, handler_type
from optic.state.actions import ClickEvent


def button(*, label: str, on_click: Callable[[Any, ClickEvent], Any]):
    """
    This function creates a button component with a label and an on_click event.

    Args:
        label (str): The text to be displayed on the button.
        on_click (Callable[..., Any]): The function to be called when the button is clicked.
    """
    insert_component(
        data=pb.ComponentData(
            button=pb.ButtonComponent(
                label=label,
                on_click=handler_type(on_click),
            )
        )
    )
