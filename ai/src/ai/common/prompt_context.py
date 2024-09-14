from ai.common.entity_store import BaseEntity, EntityStore


class PromptContext(BaseEntity):
  """
  PromptContext represents the context of a prompt.
  """

  fragment_ids: list[str]


prompt_context_store = EntityStore(PromptContext, dirname="prompt_contexts")
