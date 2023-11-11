from typing import Any, Callable
import protos.ui_pb2 as pb
from optic.lib.runtime import runtime
from optic.components.component_util import get_qualified_fn_name


def checkbox(label: str, on_update: Callable[..., Any]):
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
