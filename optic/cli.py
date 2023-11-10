import importlib.util
import traceback
from types import ModuleType

from absl import app
from absl import flags

from optic.lib.runtime import runtime
from optic import dev_server

FLAGS = flags.FLAGS

flags.DEFINE_string('path', '', 'path to main python module of Optic app.')

def main(argv):
    if len(FLAGS.path) < 1:
        raise Exception("Required flag 'path'. Received: " + FLAGS.path)
    
    module = read_module(FLAGS.path)
    assert module
    runtime.set_module(module)
    dev_server.run()

def read_module(module_path: str) -> ModuleType | None :
    try:
        spec = importlib.util.spec_from_file_location("module_name", module_path)
        assert spec
        module = importlib.util.module_from_spec(spec)
        assert spec.loader
        spec.loader.exec_module(module)
    except Exception as e:
        message = f"Error loading module '{module_path}' has {e}.\n${traceback.format_exc()}"
        print(message)
        return None

    if hasattr(module, "main"):
        return module
    else:
        print("No main function found")
        return None


if __name__ == '__main__':
    app.run(main)

