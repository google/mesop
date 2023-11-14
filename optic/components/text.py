import protos.ui_pb2 as pb
from optic.lib.runtime import runtime


def text(*, text: str):
    runtime.session().current_node().children.append(
        pb.Component(data=pb.ComponentData(text=pb.TextComponent(text=text)))
    )
