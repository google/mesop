from typing import get_args, get_type_hints

import mesop as me
from ai.common.model import model_store
from ai.common.producer import (
  Producer,
)
from ai.common.producer import (
  producer_store as store,
)
from ai.common.prompt_context import prompt_context_store
from ai.console.pages.add_edit_page_helper import (
  create_add_edit_page,
  form_field,
  get_field_value,
  update_state,
)

producer_type_hints = get_type_hints(Producer)
output_format_type = producer_type_hints["output_format"]
output_format_options = list(get_args(output_format_type))


def get_model_ids():
  options: list[me.AutocompleteOption] = []

  for model in model_store.get_all():
    options.append(me.AutocompleteOption(label=model.id, value=model.id))

  return options


def get_prompt_context_ids():
  options: list[me.AutocompleteOption] = []

  for prompt_context in prompt_context_store.get_all():
    options.append(
      me.AutocompleteOption(label=prompt_context.id, value=prompt_context.id)
    )

  return options


def form():
  form_field("id", "Unique identifier for the producer")
  me.autocomplete(
    value=get_field_value("mesop_model_id"),
    label="Model id",
    options=get_model_ids(),
    style=me.Style(width="min(100%, 360px)"),
    on_selection_change=lambda e: update_state("mesop_model_id", e.value),
  )
  me.autocomplete(
    value=get_field_value("prompt_context_id"),
    label="Prompt context id",
    options=get_prompt_context_ids(),
    style=me.Style(width="min(100%, 360px)"),
    on_selection_change=lambda e: update_state("prompt_context_id", e.value),
  )

  me.select(
    value=get_field_value("output_format"),
    label="Output format",
    options=[
      me.SelectOption(label=option.capitalize(), value=option)
      for option in output_format_options
    ],
    on_selection_change=lambda e: update_state("output_format", e.value),
    style=me.Style(width="min(100%, 360px)"),
  )
  form_field("temperature", "temperature (default 0.8)", type="number")


create_add_edit_page(
  store=store,
  entity_type=Producer,
  entity_name="Producer",
  root_path="/producers",
  form=form,
)
