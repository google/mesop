from typing import Any, Generator, TypeVar, Callable, Type, cast

from optic.key import key_from_proto

from optic.exceptions import OpticInternalException
import optic.events as events
from ..component_helpers.helper import get_qualified_fn_name
from optic.runtime import runtime
import protos.ui_pb2 as pb

A = TypeVar("A")
Handler = Callable[[A], None | Generator[None, None, None]]


def event_handler(actionType: Type[A]) -> Callable[[Handler[A]], Handler[A]]:
    """
    Decorator for making a function into an event handler."""

    def register(func: Handler[A]):
        def wrapper(action: A):
            # This is guaranteed to be a UserEvent because only Optic
            # framework will call the wrapper.
            proto_event = cast(pb.UserEvent, action)
            key = key_from_proto(proto_event.key)

            if actionType == events.CheckboxEvent:
                event = events.CheckboxEvent(checked=proto_event.bool, key=key)
            elif actionType == events.ChangeEvent:
                event = events.ChangeEvent(key=key, value=proto_event.string)
            elif actionType == events.ClickEvent:
                event = events.ClickEvent()
            else:
                raise OpticInternalException("Unhandled event type: " + str(actionType))

            return func(cast(Any, event))

        wrapper.__module__ = func.__module__
        wrapper.__name__ = func.__name__

        runtime.register_handler(get_qualified_fn_name(func), wrapper)
        return wrapper

    return register
