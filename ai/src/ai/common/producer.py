from pydantic import field_validator

from ai.common.entity_store import BaseEntity, EntityStore
from ai.common.model_validators import is_required_str
from ai.common.output_format import OutputFormat

_TEMPERATURE_DEFAULT = 0.8


class Producer(BaseEntity):
  mesop_model_id: str  # using model_id has a conflict with Pydantic
  prompt_context_id: str
  output_format: OutputFormat = "diff"
  temperature: float = _TEMPERATURE_DEFAULT

  @field_validator("mesop_model_id", "prompt_context_id", mode="after")
  @classmethod
  def is_required(cls, v):
    return is_required_str(v)

  @field_validator("temperature", mode="before")
  @classmethod
  # Intentionally leave out annotations since the input value may be ambiguous.
  def convert_empty_string_to_defaults(cls, v):
    if isinstance(v, str) and v == "":
      return _TEMPERATURE_DEFAULT
    return v


producer_store = EntityStore(Producer, dirname="producers")
