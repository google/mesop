from typing import Optional

from pydantic import BaseModel

from ai.common.entity_store import EntityStore


class FineTunedModelProperties(BaseModel):
  """
  FineTunedModelProperties represents the properties of a fine-tuned model.

  name is a descriptive name of the purpose/intent of the fine-tuning.
  """

  name: str
  provider_url: str
  wandb_url: str


class ModelPricing(BaseModel):
  """
  ModelPricing represents the pricing of a model.
  """

  dollars_per_million_input_tokens: float
  dollars_per_million_output_tokens: float


class Model(BaseModel):
  """
  Model represents an LLM.

  id must be unqiue.
  - For vanilla models: `$Provider_$ModelName_$date_$counter`
  - For fine-tuned models: `$Provider_$ModelName_ft_$ftname_$date_$counter`

  Name should match the model name used by the provider for the API call.
  """

  id: str
  name: str
  provider: str
  fine_tuned: Optional[FineTunedModelProperties] = None
  pricing: Optional[ModelPricing] = None


model_store = EntityStore(Model, dirname="models")
