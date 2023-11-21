import importlib.util
from types import ModuleType


def read_module(module_path: str) -> ModuleType:
    try:
        spec = importlib.util.spec_from_file_location("module_name", module_path)
        assert spec
        module = importlib.util.module_from_spec(spec)
        assert spec.loader
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        raise e
