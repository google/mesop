import importlib.util
import sys
from types import ModuleType

# Keep track of modules loaded by the Mesop application, so that we can
# clear the module cache when hot reloading.
_app_modules: set[str] = set()


def execute_module(module_path: str) -> ModuleType:
  global _app_modules
  # Delete all modules that were added after we loaded the module
  # so that when we reload the module, we re-execute any imported modules
  # from the main app module.
  for module_name in _app_modules:
    del sys.modules[module_name]

  # Keep track of all the sys modules in a set
  # so we can compare it after we load the module
  # to see what modules were added.
  pre_load_modules = set(sys.modules.keys())

  spec = importlib.util.spec_from_file_location("main_mesop_app", module_path)
  assert spec
  module = importlib.util.module_from_spec(spec)
  assert spec.loader
  spec.loader.exec_module(module)

  # Get the set of modules that were added after we loaded the module
  _app_modules = set(sys.modules.keys()) - pre_load_modules

  return module
