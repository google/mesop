from mesop.runtime import enable_debug_mode
from mesop.server.constants import EDITOR_PACKAGE_PATH, PROD_PACKAGE_PATH
from mesop.server.logging import log_startup
from mesop.server.server import configure_flask_app
from mesop.server.static_file_serving import configure_static_file_serving


def run(*, port: int = 32123, prod_mode: bool = True):
  flask_app = configure_flask_app()

  if prod_mode:
    enable_debug_mode()

  configure_static_file_serving(
    flask_app,
    static_file_runfiles_base=PROD_PACKAGE_PATH
    if prod_mode
    else EDITOR_PACKAGE_PATH,
  )

  log_startup(port=port)

  flask_app.run(host="0.0.0.0", port=port, use_reloader=False)
