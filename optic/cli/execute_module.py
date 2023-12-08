import importlib.util
from types import ModuleType


def execute_module(module_path: str) -> ModuleType:
  spec = importlib.util.spec_from_file_location("main_optic_app", module_path)
  assert spec
  module = importlib.util.module_from_spec(spec)
  assert spec.loader
  spec.loader.exec_module(module)

  return module
