from dataclasses import dataclass
from typing import Any, Callable

import protos.ui_pb2 as pb
from .session import Session
from optic.store import Store
from optic.exceptions import OpticUserException

Handler = Callable[[Any], None]
newline = "\n"


@dataclass
class EmptyState:
    pass


class Runtime:
    _session: Session
    _path_fns: dict[str, Callable[[], None]]
    _handlers: dict[str, Handler]
    _state_class: Any | None
    _loading_errors: list[pb.ServerError]

    def __init__(self):
        self._path_fns = {}
        self._handlers = {}
        self._state_class = None
        self._loading_errors = []

    def session(self):
        return self._session

    def reset_session(self):
        if self._state_class is None:
            print("No state class was registered, using an empty state")
            state = EmptyState()
        else:
            state = self._state_class()
        # Create a new instance of State so that we don't accidentally share state across sessions.
        self._session = Session(Store(state, self.get_handler))

    def run_path(self, path: str) -> None:
        if path not in self._path_fns:
            paths = list(self._path_fns.keys())
            paths.sort()
            raise OpticUserException(
                f"""Accessed path: {path} not registered

Try one of the following paths:
{newline.join(paths)}
                                     """
            )
        self._path_fns[path]()

    def register_path_fn(self, path: str, fn: Callable[[], None]) -> None:
        self._path_fns[path] = fn

    def register_handler(self, handler_id: str, handler: Handler) -> None:
        self._handlers[handler_id] = handler

    def get_handler(self, handler_id: str) -> Handler | None:
        return self._handlers[handler_id]

    def set_state_class(self, state_class: Any) -> None:
        self._state_class = state_class

    def add_loading_error(self, error: pb.ServerError) -> None:
        """Only put non-session specific errors, because these errors can be potentially shown across sessions."""
        self._loading_errors.append(error)

    def has_loading_errors(self) -> bool:
        return len(self._loading_errors) > 0

    def get_loading_errors(self) -> list[pb.ServerError]:
        return self._loading_errors


runtime = Runtime()
