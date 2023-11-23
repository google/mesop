from typing import Any, TypeVar, Callable, Type, cast

from optic.key import key_from_proto

import optic.events as events
from ..component_helpers.helper import get_qualified_fn_name
from optic.runtime import runtime
import protos.ui_pb2 as pb

A = TypeVar("A")
Handler = Callable[[A], None]


def event_handler(actionType: Type[A]) -> Callable[[Handler[A]], Handler[A]]:
    """
    Decorator for making a function into an event handler."""

    def register(func: Handler[A]):
        def wrapper(action: A):
            # This is guaranteed to be a UserEvent because only Optic
            # framework will call the wrapper.
            typed_action = cast(pb.UserEvent, action)
            key = key_from_proto(typed_action.key)

            if actionType == events.CheckboxEvent:
                typed_action = events.CheckboxEvent(checked=typed_action.bool, key=key)

            return func(cast(Any, typed_action))

        wrapper.__module__ = func.__module__
        wrapper.__name__ = func.__name__

        runtime.register_handler(get_qualified_fn_name(func), wrapper)
        return wrapper

    return register
