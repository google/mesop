from typing import Any, Callable
import protos.ui_pb2 as pb
from optic.components.helper import insert_component, handler_type
from optic.state.actions import CheckboxEvent


def checkbox(*, label: str, on_update: Callable[[Any, CheckboxEvent], Any]):
    """
    Creates a checkbox component with a specified label and update action.

    Args:
        label (str): The label for the checkbox.
        on_update (Callable[..., Any]): The function to be called when the checkbox is updated.

    The function appends the created checkbox component to the children of the current node in the runtime session.
    """
    insert_component(
            data=pb.ComponentData(
                checkbox=pb.CheckboxComponent(
                    label=label,
                    on_update=handler_type(on_update),
                )
            )
    )
