from ai.common.model import (
  Model,
)
from ai.common.model import (
  model_store as store,
)
from ai.console.pages.add_edit_page_helper import (
  create_add_edit_page,
  form_field,
)


def form():
  form_field("provider", "Provider of the model")
  form_field("name", "Descriptive name for the model")
  form_field("id", "Unique identifier for the model")


create_add_edit_page(
  store=store,
  entity_type=Model,
  entity_name="Model",
  root_path="/models",
  form=form,
)
