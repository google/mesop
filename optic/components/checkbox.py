from typing import Any, Callable
import protos.ui_pb2 as pb
from optic.lib.runtime import runtime
from optic.components.component_util import get_qualified_fn_name

from optic.state.actions import CheckboxEvent

def checkbox(*, label: str, on_update: Callable[[Any, CheckboxEvent], Any]):
    """
    Creates a checkbox component with a specified label and update action.

    Args:
        label (str): The label for the checkbox.
        on_update (Callable[..., Any]): The function to be called when the checkbox is updated.

    The function appends the created checkbox component to the children of the current node in the runtime session.
    """
    runtime.session().current_node().children.append(
        pb.Component(
            data=pb.ComponentData(
                checkbox=pb.CheckboxComponent(
                    label=label,
                    on_update=pb.ActionType(type=get_qualified_fn_name(on_update)),
                )
            )
        )
    )
