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

  state_session_backend: Literal[
    "memory", "file", "firestore", "sql", "none"
  ] = "none"
  state_session_backend_file_base_dir: Path = Path("/tmp")
  state_session_backend_firestore_collection: str = "mesop_state_sessions"
  state_session_backend_sql_connection_uri: str = ""
  state_session_backend_sql_table: str = "mesop_state_sessions"

  @property
  def state_session_enabled(self):
    return self.state_session_backend != "none"


def CreateConfigFromEnv() -> Config:
  file_base_dir = os.getenv("MESOP_STATE_SESSION_BACKEND_FILE_BASE_DIR")

  env_vars = dict(
    state_session_backend=os.getenv("MESOP_STATE_SESSION_BACKEND"),  # type: ignore
    state_session_backend_file_base_dir=Path(file_base_dir)
    if file_base_dir
    else None,
    state_session_backend_firestore_collection=os.getenv(
      "MESOP_STATE_SESSION_BACKEND_FIRESTORE_COLLECTION"
    ),
    state_session_backend_sql_connection_uri=os.getenv(
      "MESOP_STATE_SESSION_BACKEND_SQL_CONNECTION_URI"
    ),
    state_session_backend_sql_table=os.getenv(
      "MESOP_STATE_SESSION_BACKEND_SQL_TABLE",
    ),
  )

  return Config(
    **{key: value for key, value in env_vars.items() if value is not None}  # type: ignore
  )


# The app config is a singleton object.
app_config = CreateConfigFromEnv()
