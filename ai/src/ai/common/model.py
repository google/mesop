from pydantic import BaseModel

from ai.common.entity_store import EntityStore


class Model(BaseModel):
  """
  Model represents an LLM.
  Name should match the model name used by the provider for the API call.
  """

  id: str
  name: str
  provider: str


model_store = EntityStore(Model, dirname="models")
