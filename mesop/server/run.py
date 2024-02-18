from absl import app

from mesop.runtime import enable_debug_mode
from mesop.server.constants import EDITOR_PACKAGE_PATH
from mesop.server.flags import port
from mesop.server.logging import log_startup
from mesop.server.server import configure_flask_app
from mesop.server.static_file_serving import configure_static_file_serving


def run():
  app.run(inner_run)


def inner_run(argv):
  flask_app = configure_flask_app()
  enable_debug_mode()
  configure_static_file_serving(
    flask_app, static_file_runfiles_base=EDITOR_PACKAGE_PATH
  )

  log_startup()

  flask_app.run(host="0.0.0.0", port=port(), use_reloader=False)
