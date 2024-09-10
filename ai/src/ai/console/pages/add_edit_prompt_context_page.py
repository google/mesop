from functools import partial

import mesop as me
from ai.common.prompt_context import (
  PromptContext,
)
from ai.common.prompt_context import (
  prompt_context_store as store,
)
from ai.common.prompt_fragment import (
  prompt_fragment_store,
)
from ai.console.pages.add_edit_page_helper import (
  create_add_edit_page,
  form_field,
  get_field_value,
  update_state,
)


def update_fragment_id(e: me.SelectSelectionChangeEvent, index: int):
  fragment_ids = get_field_value("fragment_ids")
  fragment_ids[index] = e.value
  update_state("fragment_ids", fragment_ids)


def delete_fragment_id(e: me.ClickEvent, index: int):
  fragment_ids = get_field_value("fragment_ids")
  fragment_ids.pop(index)
  update_state("fragment_ids", fragment_ids)


def append_fragment_id(e: me.SelectSelectionChangeEvent):
  fragment_ids = get_field_value("fragment_ids")
  if fragment_ids is None or fragment_ids == "":
    fragment_ids = []
  fragment_ids.append(e.value)
  update_state("fragment_ids", fragment_ids)


def form():
  form_field("id", "Unique identifier")
  fragment_ids = get_field_value("fragment_ids")
  for index, fragment_id in enumerate(fragment_ids):
    with me.box(style=me.Style(display="flex", gap=8)):
      me.select(
        value=fragment_id,
        label="Fragment IDs",
        options=get_fragment_options(),
        style=me.Style(width="360px"),
        on_selection_change=partial(update_fragment_id, index=index),
      )
      me.button(
        "Remove",
        on_click=partial(delete_fragment_id, index=index),
      )
  me.select(
    label="Fragment IDs",
    options=get_fragment_options(),
    style=me.Style(width="min(100%, 360px)"),
    on_selection_change=append_fragment_id,
  )


def get_fragment_options():
  return [
    me.SelectOption(label=fragment.id, value=fragment.id)
    for fragment in prompt_fragment_store.get_all()
  ]


create_add_edit_page(
  store=store,
  entity_type=PromptContext,
  entity_name="Prompt Context",
  root_path="/prompt-contexts",
  form=form,
)
