import importlib.util
from types import ModuleType

from absl import app
from absl import flags

from optic.lib.runtime import runtime
from optic.server import dev_server

FLAGS = flags.FLAGS

flags.DEFINE_string('path', '', 'path to main python module of Optic app.')

def main(argv):
    if len(FLAGS.path) < 1:
        raise Exception("Required flag 'path'. Received: " + FLAGS.path)
    
    runtime.set_load_module(lambda: read_module(FLAGS.path))
    dev_server.run()

def read_module(module_path: str) -> ModuleType :
    try:
        spec = importlib.util.spec_from_file_location("module_name", module_path)
        assert spec
        module = importlib.util.module_from_spec(spec)
        assert spec.loader
        spec.loader.exec_module(module)
    except Exception as e:
        raise e

    if hasattr(module, "main"):
        return module
    else:
        raise Exception("No main function found")
        


if __name__ == '__main__':
    app.run(main)

