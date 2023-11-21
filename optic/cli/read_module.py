import importlib.util
import sys
from types import ModuleType


def read_module(module_path: str) -> ModuleType:
    try:
        # Keep track of all the sys modules in a set
        # so we can compare it after we load the module
        # to see what modules were added.
        pre_load_modules = set(sys.modules.keys())

        spec = importlib.util.spec_from_file_location("main_optic_app", module_path)
        assert spec
        module = importlib.util.module_from_spec(spec)
        assert spec.loader
        spec.loader.exec_module(module)

        # Get the set of modules that were added after we loaded the module
        post_load_modules = set(sys.modules.keys()) - pre_load_modules
        # Delete all modules that were added after we loaded the module
        # so that when we reload the module, we re-execute any imported modules
        # from the main app module.
        for module_name in post_load_modules:
            del sys.modules[module_name]

        return module
    except Exception as e:
        raise e
