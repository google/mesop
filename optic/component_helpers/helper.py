from typing import Any, Callable, Type, TypeVar

import optic.protos.ui_pb2 as pb
from optic.events import OpticEvent
from optic.key import Key
from optic.runtime import runtime


class ComponentWithChildren:
  def __init__(
    self,
    component: pb.Component,
  ):
    self.prev_current_node = runtime().context().current_node()
    self.component = component

  def __enter__(self):
    runtime().context().set_current_node(self.component)
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):  # type: ignore
    # TODO: not sure why I can't append this in `__enter__`
    runtime().context().set_current_node(self.prev_current_node)
    self.prev_current_node.children.append(self.component)


def insert_component(type: pb.Type, key: str | None = None):
  """
  Inserts a component into the current context's current node.
  """

  runtime().context().current_node().children.append(
    pb.Component(key=pb.Key(key=key) if key else None, type=type)
  )


def handler_type(handler_fn: Callable[..., Any]) -> str:
  return get_qualified_fn_name(handler_fn)


def get_qualified_fn_name(fn: Callable[..., Any]) -> str:
  return f"{fn.__module__}.{fn.__name__}"


E = TypeVar("E", bound=OpticEvent)


def register_event_mapper(
  event: Type[E], map_fn: Callable[[pb.UserEvent, Key], E]
):
  runtime().register_event_mapper(event=event, map_fn=map_fn)
