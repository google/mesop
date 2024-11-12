import os

from mesop.exceptions import MesopDeveloperException

AI_SERVICE_BASE_URL = os.environ.get(
  "MESOP_AI_SERVICE_BASE_URL", "http://localhost:43234"
)

MESOP_APP_BASE_PATH = os.environ.get("MESOP_APP_BASE_PATH", "")
if MESOP_APP_BASE_PATH:
  if not os.path.isabs(MESOP_APP_BASE_PATH):
    raise MesopDeveloperException(
      f"MESOP_APP_BASE_PATH must be an absolute path, but got {MESOP_APP_BASE_PATH} instead."
    )
  if not os.path.isdir(MESOP_APP_BASE_PATH):
    raise MesopDeveloperException(
      f"MESOP_APP_BASE_PATH is not a valid directory: {MESOP_APP_BASE_PATH}"
    )


def get_app_base_path() -> str:
  if not MESOP_APP_BASE_PATH:
    return os.getcwd()
  return MESOP_APP_BASE_PATH


MESOP_WEBSOCKETS_ENABLED = (
  os.environ.get("MESOP_WEBSOCKETS_ENABLED", "false").lower() == "true"
)

MESOP_CONCURRENT_UPDATES_ENABLED = (
  os.environ.get("MESOP_CONCURRENT_UPDATES_ENABLED", "false").lower() == "true"
)

if MESOP_WEBSOCKETS_ENABLED:
  MESOP_CONCURRENT_UPDATES_ENABLED = True


EXPERIMENTAL_EDITOR_TOOLBAR_ENABLED = (
  os.environ.get("MESOP_EXPERIMENTAL_EDITOR_TOOLBAR", "false").lower() == "true"
)
