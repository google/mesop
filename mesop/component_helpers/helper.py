from typing import Any, Callable, Type, TypeVar

from google.protobuf import json_format
from google.protobuf.message import Message

import mesop.protos.ui_pb2 as pb
from mesop.events import MesopEvent
from mesop.key import Key
from mesop.runtime import runtime


class _ComponentWithChildren:
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
  variant_index = 0
  # This is not exactly type-safe, but it's a convenient way of grabbing the
  # variant index value.
  if hasattr(proto, "variant_index"):
    variant_index = proto.variant_index  # type: ignore
  type = pb.Type(
    name=type_name,
    value=proto.SerializeToString(),
    variant_index=variant_index,  # type: ignore
  )
  if runtime().debug_mode:
    type.debug_json = json_format.MessageToJson(
      proto, preserving_proto_field_name=True
    )

  return pb.Component(key=pb.Key(key=key) if key else None, type=type)


def insert_composite_component(
  type_name: str,
  proto: Message,
  key: str | None = None,
) -> _ComponentWithChildren:
  return _ComponentWithChildren(type_name=type_name, proto=proto, key=key)


def insert_component(
  type_name: str,
  proto: Message,
  key: str | None = None,
) -> None:
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
