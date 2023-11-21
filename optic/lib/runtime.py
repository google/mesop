from types import ModuleType
from typing import Callable
from .session import Session


class Runtime:
    _session: Session

    def __init__(self):
        self._session = Session()

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
        self._session.run_path(path)


runtime = Runtime()
