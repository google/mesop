from types import ModuleType
from typing import Any, Callable
from .session import Session

Handler = Callable[[Any, Any], None]


class Runtime:
    _session: Session
    _path_fns: dict[str, Callable[[], None]]
    _handlers: dict[str, Handler]

    def __init__(self):
        self.reset_session()
        self._path_fns = {}
        self._handlers = {}

    def session(self):
        return self._session

    def reset_session(self):
        self._session = Session(self.get_handler)

    def set_load_module(self, load_module: Callable[[], ModuleType]) -> None:
        self._load_module = load_module

    def load_module(self) -> None:
        self._module = self._load_module()

    def run_path(self, path: str) -> None:
        # Make sure we've loaded the module, otherwise no paths will be registered
        # with the session.
        assert self._module
        self._path_fns[path]()

    def register_path_fn(self, path: str, fn: Callable[[], None]) -> None:
        self._path_fns[path] = fn

    def register_handler(self, handler_id: str, handler: Handler) -> None:
        self._handlers[handler_id] = handler

    def get_handler(self, handler_id: str) -> Handler | None:
        return self._handlers[handler_id]


runtime = Runtime()
