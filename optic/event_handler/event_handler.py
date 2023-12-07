from typing import Any, Generator, TypeVar, Callable, Type, cast

from optic.key import key_from_proto

import optic.events as events
from ..component_helpers.helper import get_qualified_fn_name
from optic.runtime import runtime
import optic.protos.ui_pb2 as pb

E = TypeVar("E", bound=events.OpticEvent)
Handler = Callable[[E], None | Generator[None, None, None]]


def event_handler(actionType: Type[E]) -> Callable[[Handler[E]], Handler[E]]:
    """
    Decorator for making a function into an event handler."""

    def register(func: Handler[E]):
        def wrapper(action: E):
            # This is guaranteed to be a UserEvent because only Optic
            # framework will call the wrapper.
            proto_event = cast(pb.UserEvent, action)
            key = key_from_proto(proto_event.key)

            event = runtime.get_event_mapper(actionType)(proto_event, key)

            return func(cast(Any, event))

        wrapper.__module__ = func.__module__
        wrapper.__name__ = func.__name__

        runtime.register_handler(get_qualified_fn_name(func), wrapper)
        return wrapper

    return register


runtime.register_event_mapper(
    events.ChangeEvent,
    lambda userEvent, key: events.ChangeEvent(
        value=userEvent.string,
        key=key,
    ),
)

runtime.register_event_mapper(
    events.ClickEvent,
    lambda userEvent, key: events.ClickEvent(
        key=key,
    ),
)
