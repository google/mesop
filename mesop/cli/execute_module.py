import importlib.util
import os
import sys
from types import ModuleType

from mesop.utils.runfiles import get_runfile_location


def execute_module(*, runfile_path: str) -> ModuleType:
  module_path = get_runfile_location(runfile_path)
  module_name = get_module_name(runfile_path)

  # Delete all app modules so we reload them.
  for submodule in get_app_modules(module_name, set(sys.modules.keys())):
    del sys.modules[submodule]

  spec = importlib.util.spec_from_file_location(module_name, module_path)
  assert spec
  module = importlib.util.module_from_spec(spec)
  assert spec.loader
  spec.loader.exec_module(module)

  return module


def get_module_name(runfile_path: str) -> str:
  """
  Creates a synthetic Python module name based on the runfile path.

  Example:
  Input: "mesop/mesop/index.py"
  Output: "mesop.examples.index"
  """

  # Intentionally skip the first segment which will be the workspace root (e.g. "mesop").
  # Note: this workspace root name is different downstream.
  segments = runfile_path.split(os.path.sep)[1:]

  # Trim the filename extension (".py") from the last path segment.
  segments[len(segments) - 1] = segments[len(segments) - 1].split(".")[0]
  return ".".join(segments)


def get_app_modules(
  main_module_name: str, loaded_module_names: set[str]
) -> set[str]:
  """
  Returns all the submodules and other modules in the same package from a set of input modules.

  This is a simple heuristic to figure out which modules are part of the project, vs. transitive dependencies that
  are unlikely needed to be hot reloaded (and shouldn't in cases like numpy where it can
  cause subtle bugs).
  """

  # Remove the last segment which is the filename so we include modules in the same package.
  main_module_prefix_segments = main_module_name.split(".")[:-1]

  submodules: set[str] = set()
  for module in loaded_module_names:
    # Special case for mesop/index.py, which would normally consider
    # mesop.runtime a sub-package/sub-module, however reloading runtime
    # is problematic because it's a stateful singleton and it causes
    # strange bugs. Thus, we avoid reloading mesop.runtime modules
    # in all cases.
    if module.split(".")[:2] == ["mesop", "runtime"]:
      continue
    if (
      module.split(".")[: len(main_module_prefix_segments)]
      == main_module_prefix_segments
    ):
      submodules.add(module)
  return submodules
