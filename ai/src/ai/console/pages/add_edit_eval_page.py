import datetime
from typing import Any

import mesop as me
from ai.common.producer import producer_store
from ai.console.pages.add_edit_page_helper import (
  create_add_edit_page,
  form_field,
  get_field_value,
  update_state,
)
from ai.offline_common.eval import (
  Eval,
)
from ai.offline_common.eval import (
  eval_store as store,
)


def get_producer_ids():
  options: list[me.AutocompleteOption] = []

  for producer in producer_store.get_all():
    options.append(me.AutocompleteOption(label=producer.id, value=producer.id))

  return options


def form():
  form_field("id", "Eval id")
  me.autocomplete(
    value=get_field_value("producer_id"),
    label="Producer id",
    options=get_producer_ids(),
    style=me.Style(width="100%"),
    on_selection_change=lambda e: update_state("producer_id", e.value),
  )
  form_field("seed", "Seed (optional)", type="number")


def create_default_eval() -> dict[str, Any]:
  id = datetime.datetime.now().replace(microsecond=0).isoformat()
  return {"id": id, "producer_id": ""}


create_add_edit_page(
  store=store,
  entity_type=Eval,
  entity_name="Eval",
  root_path="/evals",
  form=form,
  create_default_entity=create_default_eval,
  disable_edit=True,
)
