from typing import Literal

from pydantic import validate_arguments

import mesop.components.form_field.form_field_pb2 as form_field_pb
from mesop.component_helpers import (
  insert_composite_component,
)


@validate_arguments
def form_field(
  *,
  key: str | None = None,
  hide_required_marker: bool = False,
  color: Literal["primary", "accent", "warn"] = "primary",
  float_label: Literal["always", "auto"] = "always",
  appearance: Literal["fill", "outline"] = "fill",
  subscript_sizing: Literal["fixed", "dynamic"] = "fixed",
  hint_label: str = "",
):
  """
  TODO_doc_string
  """
  return insert_composite_component(
    key=key,
    type_name="form_field",
    proto=form_field_pb.FormFieldType(
      hide_required_marker=hide_required_marker,
      color=color,
      float_label=float_label,
      appearance=appearance,
      subscript_sizing=subscript_sizing,
      hint_label=hint_label,
    ),
  )
