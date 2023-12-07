from pydantic import validate_arguments

import optic.protos.ui_pb2 as pb
import optic.components.text.text_pb2 as text_pb2
from optic.component_helpers import insert_component


@validate_arguments
def text(
    *,
    text: str,
    key: str | None = None,
):
    insert_component(
        key=key,
        type=pb.Type(
            name="text", value=text_pb2.TextType(text=text).SerializeToString()
        ),
    )
