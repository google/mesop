from typing import Any, Callable
from optic.runtime import runtime

import protos.ui_pb2 as pb


class ComponentWithChildren:
    def __init__(
        self,
        component: pb.Component,
    ):
        self.prev_current_node = runtime.session().current_node()
        self.component = component

    def __enter__(self):
        runtime.session().set_current_node(self.component)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):  # type: ignore
        # TODO: not sure why I can't append this in `__enter__`
        runtime.session().set_current_node(self.prev_current_node)
        self.prev_current_node.children.append(self.component)


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
