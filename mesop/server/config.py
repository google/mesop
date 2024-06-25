import os
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Config(BaseModel):
  """Mesop app configuration."""

  state_session_backend: Literal["memory", "none"] = "memory"

  @property
  def state_session_enabled(self):
    return self.state_session_backend != "none"


def CreateConfigFromEnv() -> Config:
  return Config(
    state_session_backend=os.getenv("MESOP_STATE_SESSION_BACKEND", "memory"),
  )


# The app config is a singleton object.
app_config = CreateConfigFromEnv()
