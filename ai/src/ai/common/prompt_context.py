from pydantic import BaseModel, field_validator

from ai.common.entity_store import EntityStore
from ai.common.model_validators import is_required_str


class PromptContext(BaseModel):
  """
  PromptContext represents the context of a prompt.
  """

  id: str
  fragment_ids: list[str]

  @field_validator("id", mode="after")
  @classmethod
  def is_required(cls, v):
    return is_required_str(v)


prompt_context_store = EntityStore(PromptContext, dirname="prompt_contexts")
