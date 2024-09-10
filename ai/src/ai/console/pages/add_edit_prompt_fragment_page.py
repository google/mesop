import os

import mesop as me
from ai.common.prompt_fragment import (
  PromptFragment,
)
from ai.common.prompt_fragment import (
  prompt_fragment_store as store,
)
from ai.console.pages.add_edit_page_helper import (
  create_add_edit_page,
  form_field,
  get_field_value,
  update_state,
)


def get_autocomplete_options():
  options: list[me.AutocompleteOption] = []
  prompt_contents_dir = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "..", "data", "prompt_contents"
  )
  if os.path.exists(prompt_contents_dir):
    for filename in os.listdir(prompt_contents_dir):
      file_path = os.path.join(prompt_contents_dir, filename)
      if os.path.isfile(file_path):
        options.append(
          me.AutocompleteOption(
            label=filename, value="//prompt_contents/" + filename
          )
        )

  return options


def form():
  form_field("id", "Unique identifier")
  me.select(
    value=get_field_value("role"),
    label="Role",
    options=[
      me.SelectOption(label="User", value="user"),
      me.SelectOption(label="Assistant", value="assistant"),
      me.SelectOption(label="System", value="system"),
    ],
    on_selection_change=lambda e: update_state("role", e.value),
    style=me.Style(width="min(100%, 360px)"),
  )
  me.divider()
  me.text("Content (set either value or path)")
  me.textarea(
    value=get_field_value("content_value"),
    appearance="outline",
    label="Content value",
    on_blur=lambda e: update_state(e.key, e.value),
    key="content_value",
    # TODO: potentially support golden example variables
    # for more powerful few-shot prompting, e.g. <EXAMPLE:$EXAMPLE_ID>
    hint_label="Variables: <APP_CHANGES> <USER_INPUT>",
    style=me.Style(width="min(100%)"),
  )
  me.autocomplete(
    value=get_field_value("content_path"),
    label="Content path",
    options=get_autocomplete_options(),
    hint_label="(absolute) path to a file containing the content",
    style=me.Style(width="min(100%, 360px)"),
    on_selection_change=lambda e: update_state("content_path", e.value),
  )
  me.divider()
  me.checkbox(
    checked=bool(get_field_value("chain_of_thought")),
    label="Chain of thought",
    on_change=lambda e: update_state("chain_of_thought", e.checked),
  )


create_add_edit_page(
  store=store,
  entity_type=PromptFragment,
  entity_name="Prompt Fragment",
  root_path="/prompt-fragments",
  form=form,
)
