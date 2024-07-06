from dataclasses import dataclass
from typing import Literal

Role = Literal["user", "model"]


@dataclass(kw_only=True)
class ChatMessage:
  """Chat message metadata."""

  role: Role = "user"
  content: str = ""
  in_progress: bool = False
