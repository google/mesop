from pydantic import BaseModel

from ai.common.entity_store import EntityStore


class PromptContext(BaseModel):
  """
  PromptContext represents the context of a prompt.
  """

  id: str
  fragment_ids: list[str]


prompt_context_store = EntityStore(PromptContext, dirname="prompt_contexts")
