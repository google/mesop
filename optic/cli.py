import importlib.util
from types import ModuleType

from absl import app
from absl import flags

from optic.lib.runtime import runtime

FLAGS = flags.FLAGS

flags.DEFINE_string('path', '', 'path to main python module of Optic app.')
flags.DEFINE_bool('dev', False, 'if dev=False, then run in prod mode.')

def main(argv):
    if len(FLAGS.path) < 1:
        raise Exception("Required flag 'path'. Received: " + FLAGS.path)
    
    runtime.set_load_module(lambda: read_module(FLAGS.path))

    if FLAGS.dev:
        print("Running in dev mode")
        from optic.server import dev_server
        dev_server.run()
    else:
        print("Running in prod mode")
        from optic.server import prod_server
        prod_server.run()

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

