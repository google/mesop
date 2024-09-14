from typing import Literal

from pydantic import BaseModel, field_validator, model_validator

from ai.common.entity_store import EntityStore
from ai.common.model_validators import is_required_str


class PromptFragment(BaseModel):
  id: str
  content_value: str | None = None
  content_path: str | None = None
  role: Literal["user", "assistant", "system"]
  chain_of_thought: bool = False

  @field_validator("id", mode="after")
  @classmethod
  def is_required(cls, v):
    return is_required_str(v)

  @model_validator(mode="after")
  def check_content_value_or_path(self):
    if self.content_value == "":
      self.content_value = None
    if self.content_path == "":
      self.content_path = None

    content_value = self.content_value
    content_path = self.content_path
    if content_value is not None and content_path is not None:
      raise ValueError("Only one of content_value or content_path is allowed")
    if content_value is None and content_path is None:
      raise ValueError("Either content_value or content_path is required")
    return self


prompt_fragment_store = EntityStore(PromptFragment, dirname="prompt_fragments")
