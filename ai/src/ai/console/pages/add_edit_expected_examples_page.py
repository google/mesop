import mesop as me
from ai.common.example import (
  ExpectedExample,
)
from ai.common.example import (
  expected_example_store as store,
)
from ai.console.pages.add_edit_page_helper import (
  create_add_edit_page,
  form_field,
  get_field_value,
  update_state,
)


def form():
  form_field("id", "Unique identifier for the example")
  form_field("input.prompt", "Input: prompt")
  me.textarea(
    value=get_field_value("input.input_code"),
    appearance="outline",
    label="Input code",
    on_blur=lambda e: update_state(e.key, e.value),
    key="input.input_code",
    hint_label=f"Input code path: data/golden_examples/{get_field_value('id')}/input.py",
    style=me.Style(width="min(100%, 360px)"),
  )
  form_field(
    "input.line_number_target", "Input: line number target", type="number"
  )

  me.checkbox(
    checked=bool(get_field_value("expect_executable")),
    label="Expect executable",
    key="expect_executable",
    on_change=lambda e: update_state("expect_executable", e.checked),
  )
  me.checkbox(
    checked=bool(get_field_value("expect_type_checkable")),
    label="Expect type checkable",
    key="expect_type_checkable",
    on_change=lambda e: update_state("expect_type_checkable", e.checked),
  )


create_add_edit_page(
  store=store,
  entity_type=ExpectedExample,
  entity_name="Expected Example",
  root_path="/expected-examples",
  form=form,
  create_default_entity=lambda: {
    "expect_executable": True,
    "expect_type_checkable": True,
  },
)
