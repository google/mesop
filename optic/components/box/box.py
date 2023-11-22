from pydantic import validate_arguments

import protos.ui_pb2 as pb
import optic.components.box.box_pb2 as box_pb
from optic.component_helpers import insert_component


@validate_arguments
def box(
    *,
    label: str,
    key: str | None = None,
):
    """
    This function creates a box.

    Args:
        label (str): The text to be displayed
    """
    insert_component(
        key=key,
        type=pb.Type(
            name="box",
            value=box_pb.BoxType(
                label=label,
            ).SerializeToString(),
        ),
    )
