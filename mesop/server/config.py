import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Config(BaseModel):
  """Mesop app configuration."""

  state_session_backend: Literal[
    "memory", "file", "firestore", "sql", "none"
  ] = "none"
  state_session_backend_file_base_dir: Path = Path("/tmp")
  state_session_backend_firestore_collection: str = "mesop_state_sessions"
  state_session_backend_sql_connection_uri: str = ""
  state_session_backend_sql_table: str = "mesop_state_session"

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
    state_session_backend_sql_connection_uri=os.getenv(
      "MESOP_STATE_SESSION_BACKEND_SQL_CONNECTION_URI",
      "",
    ),
    state_session_backend_sql_table=os.getenv(
      "MESOP_STATE_SESSION_BACKEND_SQL_TABLE",
      "mesop_state_session",
    ),
  )


# The app config is a singleton object.
app_config = CreateConfigFromEnv()
