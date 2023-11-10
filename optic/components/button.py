import protos.ui_pb2 as pb
from optic.lib.runtime import runtime


def button(label: str, on_click: str):
    runtime.session().current_node().children.append(
        pb.Component(
            data=pb.ComponentData(
                button=pb.ButtonComponent(
                    label=label, on_click=pb.ActionType(type=on_click)
                )
            )
        )
    )
