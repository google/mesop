from typing import Any, Callable, Literal

from pydantic import validate_arguments

import mesop.components.input.input_pb2 as input_pb
from mesop.component_helpers import (
  handler_type,
  insert_component,
)
from mesop.events import InputEvent


@validate_arguments
def input(
  *,
  key: str | None = None,
  disabled: bool = False,
  id: str = "",
  placeholder: str = "",
  name: str = "",
  required: bool = False,
  type: str = "",
  user_aria_described_by: str = "",
  value: str = "",
  readonly: bool = False,
  hide_required_marker: bool = False,
  color: Literal["primary", "accent", "warn"] = "primary",
  float_label: Literal["always", "auto"] = "always",
  appearance: Literal["fill", "outline"] = "fill",
  subscript_sizing: Literal["fixed", "dynamic"] = "fixed",
  hint_label: str = "",
  label: str = "",
  on_input: Callable[[InputEvent], Any] | None = None,
  variant: Literal["matInput"] = "matInput",
):
  """
  TODO_doc_string
  """
  insert_component(
    key=key,
    type_name="input",
    proto=input_pb.InputType(
      disabled=disabled,
      id=id,
      placeholder=placeholder,
      name=name,
      required=required,
      type=type,
      user_aria_described_by=user_aria_described_by,
      value=value,
      readonly=readonly,
      hide_required_marker=hide_required_marker,
      color=color,
      float_label=float_label,
      appearance=appearance,
      subscript_sizing=subscript_sizing,
      hint_label=hint_label,
      label=label,
      on_input_handler_id=handler_type(on_input) if on_input else "",
      variant_index=_get_variant_index(variant),
    ),
  )


def _get_variant_index(variant: str) -> int:
  if variant == "matInput":
    return 0
  raise Exception("Unexpected variant: " + variant)
