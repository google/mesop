from types import ModuleType
from typing import Callable
from .session import Session


class Runtime:
    _session: Session
    _path_fns: dict[str, Callable[[], None]]

    def __init__(self):
        self._session = Session()
        self._path_fns = {}

    def session(self):
        return self._session

    def reset_session(self):
        self._session = Session()

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


runtime = Runtime()
