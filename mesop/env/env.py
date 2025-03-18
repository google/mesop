import os

from dotenv import find_dotenv, load_dotenv

from mesop.exceptions import MesopDeveloperException

if os.environ.get("BUILD_WORKSPACE_DIRECTORY"):
  # If running with Bazel, we look for `mesop/.env` from the root workspace.
  load_dotenv()
else:
  # Try to load .env file for PyPi Mesop build which should be in the user's current
  # working directory.
  load_dotenv(find_dotenv(usecwd=True))

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


MESOP_PROD_UNREDACTED_ERRORS = (
  os.environ.get("MESOP_PROD_UNREDACTED_ERRORS", "false").lower() == "true"
)

MESOP_WEBSOCKETS_ENABLED = (
  os.environ.get("MESOP_WEBSOCKETS_ENABLED", "false").lower() == "true"
)
