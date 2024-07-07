from dataclasses import dataclass
from typing import Literal, Optional

from pydantic import BaseModel

Role = Literal["user", "model"]


@dataclass(kw_only=True)
class ChatMessage:
  """Chat message metadata."""

  role: Role = "user"
  content: str = ""
  in_progress: bool = False


class Pad(BaseModel):
  """
  Pad model containing title and content.

  Attributes:
    title (str): The title of the pad.
    content (str): The content of the pad.
  """

  title: str = ""
  content: str = ""


class Output(BaseModel):
  """
  Output model containing structured response data.

  Attributes:
    intro (str): Introduction text.
    pad (Optional[Pad]): Optional pad content.
    conclusion (str): Conclusion text.
  """

  intro: str = ""
  pad: Optional[Pad] = None
  conclusion: str = ""


def get_output_json_schema():
  return Output.schema_json(indent=2)
