from typing import Any, Callable
import protos.ui_pb2 as pb
from optic.lib.runtime import runtime
from optic.components.component_util import get_qualified_fn_name


def button(label: str, on_click: Callable[..., Any]):
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
