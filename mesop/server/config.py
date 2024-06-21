import os
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Config(BaseModel):
  """Mesop app configuration."""

  secret_key: str = ""
  state_session_backend: Literal["memory", "null"] = "memory"

  @property
  def state_session_enabled(self):
    return self.state_session_backend != "null"


def CreateConfigFromEnv() -> Config:
  return Config(
    secret_key=os.getenv("MESOP_SECRET_KEY", ""),
    state_session_backend=os.getenv("MESOP_STATE_SESSION_BACKEND", "memory"),
  )


# The app config is a singleton object.
app_config = CreateConfigFromEnv()
