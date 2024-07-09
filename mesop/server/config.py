import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Config(BaseModel):
  """Mesop app configuration."""

  state_session_backend: Literal["memory", "file", "none"] = "none"
  state_session_backend_file_base_dir: Path = Path("/tmp")

  @property
  def state_session_enabled(self):
    return self.state_session_backend != "none"


def CreateConfigFromEnv() -> Config:
  return Config(
    state_session_backend=os.getenv("MESOP_STATE_SESSION_BACKEND", "none"),  # type: ignore
    state_session_backend_file_base_dir=Path(
      os.getenv("MESOP_STATE_SESSION_BACKEND_FILE_BASE_DIR", "/tmp")
    ),
  )


# The app config is a singleton object.
app_config = CreateConfigFromEnv()
