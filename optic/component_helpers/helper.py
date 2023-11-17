from typing import Any, Callable
from optic.lib.runtime import runtime

import protos.ui_pb2 as pb


def insert_component(type: pb.Type, key: str | None = None):
    """
    Inserts a component into the current session's current node.
    """
    runtime.session().current_node().children.append(
        pb.Component(key=pb.Key(key=key or ""), type=type)
    )


def handler_type(handler_fn: Callable[..., Any]) -> str:
    return get_qualified_fn_name(handler_fn)


def get_qualified_fn_name(fn: Callable[..., Any]) -> str:
    return f"{fn.__module__}.{fn.__name__}"
