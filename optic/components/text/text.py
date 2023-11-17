import protos.ui_pb2 as pb
import optic.components.text.text_pb2 as text_pb2
from optic.component_helpers import insert_component


def text(*, text: str):
    insert_component(
        type=pb.Type(
            type="text", value=text_pb2.TextComponent(text=text).SerializeToString()
        )
    )
