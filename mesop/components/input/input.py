from typing import Literal

from pydantic import validate_arguments

import mesop.components.input.input_pb2 as input_pb
from mesop.component_helpers import (
  insert_component,
)


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
      variant_index=_get_variant_index(variant),
    ),
  )


def _get_variant_index(variant: str) -> int:
  if variant == "matInput":
    return 0
  raise Exception("Unexpected variant: " + variant)
