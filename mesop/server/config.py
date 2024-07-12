import os
from pathlib import Path
from typing import Literal

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel

if os.environ.get("BUILD_WORKSPACE_DIRECTORY"):
  # If running with Bazel, we look for `mesop/.env` from the root workspace.
  load_dotenv()
else:
  # Try to load .env file for PyPi Mesop build which should be in the user's current
  # working directory.
  load_dotenv(find_dotenv(usecwd=True))


class Config(BaseModel):
  """Mesop app configuration."""

  state_session_backend: Literal["memory", "file", "firestore", "none"] = "none"
  state_session_backend_file_base_dir: Path = Path("/tmp")
  state_session_backend_firestore_collection: str = "mesop_state_sessions"

  @property
  def state_session_enabled(self):
    return self.state_session_backend != "none"


def CreateConfigFromEnv() -> Config:
  return Config(
    state_session_backend=os.getenv("MESOP_STATE_SESSION_BACKEND", "none"),  # type: ignore
    state_session_backend_file_base_dir=Path(
      os.getenv("MESOP_STATE_SESSION_BACKEND_FILE_BASE_DIR", "/tmp")
    ),
    state_session_backend_firestore_collection=os.getenv(
      "MESOP_STATE_SESSION_BACKEND_FIRESTORE_COLLECTION",
      "mesop_state_sessions",
    ),
  )


# The app config is a singleton object.
app_config = CreateConfigFromEnv()
