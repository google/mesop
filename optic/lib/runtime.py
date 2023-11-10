from types import ModuleType
from .session import Session

class Runtime:
    def __init__(self):
        self._session = Session()

    def session(self):
        return self._session
    
    def set_module(self, module: ModuleType) -> None:
        self._module = module

    def run_module(self) -> None:
        assert self._module
        self._module.main()


runtime = Runtime()
