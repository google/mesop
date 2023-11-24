from typing import Any, Callable, Generator, TypeVar, Generic, cast
import protos.ui_pb2 as pb


S = TypeVar("S")


# (Payload) -> None
Handler = Callable[[Any], Generator[None, None, None] | None]


class Store(Generic[S]):
    def __init__(self, get_handler: Callable[[str], Handler | None]):
        self.get_handler = get_handler

    def dispatch(self, action: pb.UserEvent) -> Generator[None, None, None]:
        payload = cast(Any, action)
        handler = self.get_handler(action.handler_id)
        if handler:
            result = handler(payload)
            if result is not None:
                yield from result
            else:
                yield
        else:
            print(f"Unknown handler id: {action.handler_id}")
