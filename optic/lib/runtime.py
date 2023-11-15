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

    def run_module_main(self) -> None:
        assert self._module
        self._module.main()


runtime = Runtime()
