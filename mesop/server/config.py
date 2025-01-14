import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

# Needed to ensure dotenv is loaded
import mesop.env.env  # noqa: F401


class Config(BaseModel):
  """Mesop app configuration."""

  state_session_backend: Literal[
    "memory", "file", "firestore", "sql", "none"
  ] = "none"
  state_session_backend_file_base_dir: Path = Path("/tmp")
  state_session_backend_firestore_collection: str = "mesop_state_sessions"
  state_session_backend_sql_connection_uri: str = ""
  state_session_backend_sql_table: str = "mesop_state_sessions"
  static_folder: str = ""
  static_url_path: str = "/static"

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
    static_folder=os.getenv("MESOP_STATIC_FOLDER"),
    static_url_path=os.getenv("MESOP_STATIC_URL_PATH"),
  )

  return Config(
    **{key: value for key, value in env_vars.items() if value is not None}  # type: ignore
  )


# The app config is a singleton object.
app_config = CreateConfigFromEnv()
