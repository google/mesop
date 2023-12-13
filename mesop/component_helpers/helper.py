from typing import Any, Callable, Type, TypeVar

from google.protobuf import json_format
from google.protobuf.message import Message

import mesop.protos.ui_pb2 as pb
from mesop.events import MesopEvent
from mesop.key import Key
from mesop.runtime import runtime


class ComponentWithChildren:
  def __init__(self, type_name: str, proto: Message, key: str | None = None):
    self.prev_current_node = runtime().context().current_node()
    self.component = create_component(type_name=type_name, proto=proto, key=key)

  def __enter__(self):
    runtime().context().set_current_node(self.component)
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):  # type: ignore
    # TODO: not sure why I can't append this in `__enter__`
    runtime().context().set_current_node(self.prev_current_node)
    self.prev_current_node.children.append(self.component)


def create_component(
  type_name: str, proto: Message, key: str | None = None
) -> pb.Component:
  type = pb.Type(name=type_name, value=proto.SerializeToString())
  if runtime().debug_mode:
    type.debug_json = json_format.MessageToJson(
      proto, preserving_proto_field_name=True
    )

  return pb.Component(key=pb.Key(key=key) if key else None, type=type)


def insert_component(type_name: str, proto: Message, key: str | None = None):
  """
  Inserts a component into the current context's current node.
  """
  runtime().context().current_node().children.append(
    create_component(type_name=type_name, proto=proto, key=key)
  )


def handler_type(handler_fn: Callable[..., Any]) -> str:
  return get_qualified_fn_name(handler_fn)


def get_qualified_fn_name(fn: Callable[..., Any]) -> str:
  return f"{fn.__module__}.{fn.__name__}"


E = TypeVar("E", bound=MesopEvent)


def register_event_mapper(
  event: Type[E], map_fn: Callable[[pb.UserEvent, Key], E]
):
  runtime().register_event_mapper(event=event, map_fn=map_fn)
