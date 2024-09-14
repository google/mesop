from pydantic import field_validator

from ai.common.entity_store import BaseEntity, EntityStore
from ai.common.model_validators import is_required_str


class Model(BaseEntity):
  """
  Model represents an LLM.
  Name should match the model name used by the provider for the API call.
  """

  name: str
  provider: str

  @field_validator("name", "provider", mode="after")
  @classmethod
  def is_required(cls, v):
    return is_required_str(v)


model_store = EntityStore(Model, dirname="models")
