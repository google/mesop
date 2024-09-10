from typing import Literal

from pydantic import BaseModel

from ai.common.entity_store import EntityStore


class Producer(BaseModel):
  id: str
  mesop_model_id: str  # using model_id has a conflict with Pydantic
  prompt_context_id: str
  output_format: Literal["full", "diff"]
  temperature: float = 0.8


producer_store = EntityStore(Producer, dirname="producers")
