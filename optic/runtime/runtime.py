from typing import Any, Callable
from .session import Session
from optic.store import Store
from optic.exceptions import OpticUserException

Handler = Callable[[Any, Any], None]
newline = "\n"


class Runtime:
    _session: Session
    _path_fns: dict[str, Callable[[], None]]
    _handlers: dict[str, Handler]

    def __init__(self):
        self._path_fns = {}
        self._handlers = {}

    def session(self):
        return self._session

    def reset_session(self):
        # Create a new instance of State so that we don't accidentally share state across sessions.
        self._session = Session(Store(self._state_class(), self.get_handler))

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


runtime = Runtime()
