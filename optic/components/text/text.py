import protos.ui_pb2 as pb
from optic.component_helpers import insert_component


def text(*, text: str):
    insert_component(data=pb.ComponentData(text=pb.TextComponent(text=text)))
