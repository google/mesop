import threading

from mesop.runtime import enable_debug_mode
from mesop.server.constants import EDITOR_PACKAGE_PATH
from mesop.server.flags import port
from mesop.server.logging import log_startup
from mesop.server.server import configure_flask_app
from mesop.server.static_file_serving import configure_static_file_serving
from mesop.utils.colab_utils import is_running_in_colab


def colab_run():
  """
  When running in Colab environment, this will launch the web server.

  Otherwise, this is a no-op.
  """
  if not is_running_in_colab():
    print("Not running Colab: `colab_run` is a no-op")
    return
  flask_app = configure_flask_app()
  enable_debug_mode()
  configure_static_file_serving(
    flask_app, static_file_runfiles_base=EDITOR_PACKAGE_PATH
  )

  log_startup()

  def run_flask_app():
    flask_app.run(host="0.0.0.0", port=port(), use_reloader=False)

  # Launch Flask in background thread so we don't hog up the main thread
  # for regular Colab usage.
  threading.Thread(target=run_flask_app).start()
