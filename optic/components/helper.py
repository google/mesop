from typing import Any, Callable
from optic.lib.runtime import runtime

import protos.ui_pb2 as pb


def insert_component(data: pb.ComponentData):
    """
    Inserts a component into the current session's current node.
    """
    runtime.session().current_node().children.append(pb.Component(data=data))


def handler_type(handler_fn: Callable[..., Any]) -> pb.ActionType:
    return pb.ActionType(type=get_qualified_fn_name(handler_fn))


def get_qualified_fn_name(fn: Callable[..., Any]) -> str:
    return f"{fn.__module__}.{fn.__name__}"
