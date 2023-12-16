from typing import Any, Callable, Generator, Type, TypeVar, cast

import mesop.events as events
import mesop.protos.ui_pb2 as pb
from mesop.key import key_from_proto
from mesop.runtime import runtime

from ..component_helpers.helper import get_qualified_fn_name

E = TypeVar("E", bound=events.MesopEvent)
Handler = Callable[[E], None | Generator[None, None, None]]


def event_handler(actionType: Type[E]) -> Callable[[Handler[E]], Handler[E]]:
  """
  Decorator for making a function into an event handler."""

  def register(func: Handler[E]):
    def wrapper(action: E):
      # This is guaranteed to be a UserEvent because only Mesop
      # framework will call the wrapper.
      proto_event = cast(pb.UserEvent, action)
      key = key_from_proto(proto_event.key)

      event = runtime().get_event_mapper(actionType)(proto_event, key)

      return func(cast(Any, event))

    wrapper.__module__ = func.__module__
    wrapper.__name__ = func.__name__

    runtime().register_handler(get_qualified_fn_name(func), wrapper)
    return wrapper

  return register


runtime().register_event_mapper(
  events.ChangeEvent,
  lambda userEvent, key: events.ChangeEvent(
    value=userEvent.string,
    key=key,
  ),
)

runtime().register_event_mapper(
  events.ClickEvent,
  lambda userEvent, key: events.ClickEvent(
    key=key,
  ),
)

runtime().register_event_mapper(
  events.InputEvent,
  lambda userEvent, key: events.InputEvent(
    value=userEvent.string,
    key=key,
  ),
)
