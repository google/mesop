from pydantic import validate_arguments

from optic.lib.runtime import runtime

import protos.ui_pb2 as pb
import optic.components.box.box_pb2 as box_pb


class Box:
    def __init__(
        self,
        box: box_pb.BoxType,
        key: str,
    ):
        self.prev_current_node = runtime.session().current_node()
        self.component = pb.Component(
            key=pb.Key(key=key),
            type=pb.Type(name="box", value=box.SerializeToString()),
        )

    def __enter__(self):
        runtime.session().set_current_node(self.component)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):  # type: ignore
        # TODO: not sure why I can't append this in `__enter__`
        self.prev_current_node.children.append(self.component)
        runtime.session().set_current_node(self.prev_current_node)


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
    return Box(key=key or "", box=box_pb.BoxType(label=label))
