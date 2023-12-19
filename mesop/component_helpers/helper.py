import hashlib
import inspect
from typing import Any, Callable, Generator, Type, TypeVar, cast

from google.protobuf import json_format
from google.protobuf.message import Message

import mesop.protos.ui_pb2 as pb
from mesop.events import ChangeEvent, ClickEvent, InputEvent, MesopEvent
from mesop.key import Key, key_from_proto
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


class _UserCompositeComponent:
  def __init__(self, fn: Callable[[], Any]):
    self.prev_current_node = runtime().context().current_node()
    fn()

  def __enter__(self):
    current_children = runtime().context().current_node().children
    runtime().context().set_current_node(
      current_children[len(current_children) - 1]
    )
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):  # type: ignore
    runtime().context().set_current_node(self.prev_current_node)


def composite(fn: Callable[..., Any]):
  def wrapper(*args: Any, **kwargs: Any):
    return _UserCompositeComponent(lambda: fn(*args, **kwargs))

  return wrapper


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


E = TypeVar("E", bound=MesopEvent)
Handler = Callable[[E], None | Generator[None, None, None]]


def wrap_handler_with_event(func: Handler[E], actionType: Type[E]):
  def wrapper(action: E):
    # This is guaranteed to be a UserEvent because only Mesop
    # framework will call the wrapper.
    proto_event = cast(pb.UserEvent, action)
    key = key_from_proto(proto_event.key)

    event = runtime().get_event_mapper(actionType)(proto_event, key)

    return func(cast(Any, event))

  wrapper.__module__ = func.__module__
  wrapper.__name__ = func.__name__

  return wrapper


def register_event_handler(
  handler_fn: Callable[..., Any], event: Type[Any]
) -> str:
  fn_id = compute_fn_id(handler_fn)

  runtime().context().register_event_handler(
    fn_id, wrap_handler_with_event(handler_fn, event)
  )
  return fn_id


def compute_fn_id(fn: Callable[..., Any]) -> str:
  # Hashing id...
  source_code = inspect.getsource(fn)
  input = f"{fn.__module__}.{fn.__name__}.{source_code}"

  return hashlib.sha256(input.encode()).hexdigest()


def get_qualified_fn_name(fn: Callable[..., Any]) -> str:
  return f"{fn.__module__}.{fn.__name__}"


def register_event_mapper(
  event: Type[E], map_fn: Callable[[pb.UserEvent, Key], E]
):
  runtime().register_event_mapper(event=event, map_fn=map_fn)


runtime().register_event_mapper(
  ChangeEvent,
  lambda userEvent, key: ChangeEvent(
    value=userEvent.string,
    key=key.key,
  ),
)

runtime().register_event_mapper(
  ClickEvent,
  lambda userEvent, key: ClickEvent(
    key=key.key,
  ),
)

runtime().register_event_mapper(
  InputEvent,
  lambda userEvent, key: InputEvent(
    value=userEvent.string,
    key=key.key,
  ),
)
