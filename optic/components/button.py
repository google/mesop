from typing import Any, Callable
import protos.ui_pb2 as pb
from optic.lib.runtime import runtime
from optic.components.component_util import get_qualified_fn_name
from optic.state.actions import ClickEvent


def button(label: str, on_click: Callable[[Any, ClickEvent], Any]):
    """
    This function creates a button component with a label and an on_click event.

    Args:
        label (str): The text to be displayed on the button.
        on_click (Callable[..., Any]): The function to be called when the button is clicked.
    """
    runtime.session().current_node().children.append(
        pb.Component(
            data=pb.ComponentData(
                button=pb.ButtonComponent(
                    label=label,
                    on_click=pb.ActionType(type=get_qualified_fn_name(on_click)),
                )
            )
        )
    )
