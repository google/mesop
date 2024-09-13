import base64

import requests

import mesop as me
from ai.common.diff import apply_patch
from ai.common.example import (
  GoldenExample,
)
from ai.common.example import (
  golden_example_store as store,
)
from ai.console.pages.add_edit_page_helper import (
  create_add_edit_page,
  form_field,
  get_field_value,
  update_state,
)
from ai.offline_common.eval import SANDBOX_URL


@me.stateclass
class State:
  preview_url: str
  preview_error: str


def load_preview(e: me.ClickEvent):
  state = me.state(State)
  code = get_field_value("output.output_code")
  result = requests.post(
    SANDBOX_URL + "/exec",
    data={"code": base64.b64encode(code.encode("utf-8"))},
  )
  if result.status_code == 200:
    url_path = result.content.decode("utf-8")
    state.preview_url = SANDBOX_URL + url_path
    state.preview_error = ""
  else:
    state.preview_error = result.content.decode("utf-8")


def form():
  state = me.state(State)
  me.button("Load preview", on_click=load_preview, type="flat")
  if state.preview_url:
    me.link(
      text="Open preview",
      url=state.preview_url,
      style=me.Style(color=me.theme_var("primary"), text_decoration="none"),
      open_in_new_tab=True,
    )
  if state.preview_error:
    me.text(
      state.preview_error,
      style=me.Style(font_family="monospace", white_space="pre"),
    )

  form_field("id", "Unique identifier for the example")
  form_field("input.prompt", "Input: prompt")
  me.textarea(
    value=get_field_value("input.input_code"),  # type: ignore
    appearance="outline",
    label="Input code",
    on_blur=lambda e: update_state(e.key, e.value),
    key="input.input_code",
    hint_label=f"Input code path: data/expected_examples/{get_field_value('id')}/input.py",
    style=me.Style(width="100%"),
  )
  form_field(
    "input.line_number_target", "Input: line number target", type="number"
  )
  me.select(  # update
    value=get_field_value("output.output_type"),  # type: ignore
    options=[
      me.SelectOption(label="Full", value="full"),
      me.SelectOption(label="Diff", value="diff"),
    ],
    on_selection_change=lambda e: update_state(e.key, e.value),
    key="output.output_type",
    label="Output type",
    style=me.Style(width="min(100%, 360px)"),
  )
  me.textarea(
    value=get_field_value("output.raw_output"),  # type: ignore
    appearance="outline",
    label="Raw output",
    on_blur=update_raw_output,
    key="output.raw_output",
    hint_label=f"Output code path: data/expected_examples/{get_field_value('id')}/raw_output.txt",
    style=me.Style(width="100%"),
  )
  me.textarea(
    readonly=True,
    value=get_field_value("output.output_code"),  # type: ignore
    appearance="outline",
    label="Generated output code (read-only)",
    hint_label=f"Output code path: data/expected_examples/{get_field_value('id')}/output.py",
    style=me.Style(width="100%"),
  )


def update_raw_output(e: me.InputBlurEvent):
  update_state(e.key, e.value)
  output_type = get_field_value("output.output_type")
  if output_type == "full":
    update_state("output.output_code", e.value)
  elif output_type == "diff":
    result = apply_patch(get_field_value("input.input_code"), e.value)
    update_state("output.output_code", result.result)
  else:
    raise ValueError(f"Unknown output type: {output_type}")


create_add_edit_page(
  store=store,
  entity_type=GoldenExample,
  entity_name="Golden Example",
  root_path="/golden-examples",
  form=form,
  create_default_entity=lambda: {
    "output": {
      "output_type": "diff",
    },
  },
)
