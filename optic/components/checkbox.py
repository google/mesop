import protos.ui_pb2 as pb
from optic.lib.runtime import runtime

def checkbox(label: str):
    runtime.session().current_node().children.append(
        pb.Component(data=pb.ComponentData(checkbox=pb.CheckboxComponent(label=label)))
    )
