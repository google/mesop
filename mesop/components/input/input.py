from dataclasses import dataclass
from typing import Any, Callable, Literal, cast

from pydantic import validate_arguments

import mesop.components.input.input_pb2 as input_pb
from mesop.component_helpers import (
  insert_component,
  register_event_handler,
)
from mesop.events import InputEvent


@dataclass
class Textarea:
  """
  Represents a multi-line text input control.

  Attributes:
      rows: The number of lines to show in the text area.
  """

  rows: int = 5


@validate_arguments
def input(
  *,
  key: str | None = None,
  disabled: bool = False,
  id: str = "",
  placeholder: str = "",
  name: str = "",
  required: bool = False,
  type: Literal[
    "",
    "color",
    "date",
    "datetime-local",
    "email",
    "month",
    "number",
    "password",
    "search",
    "tel",
    "text",
    "time",
    "url",
    "week",
  ]
  | Textarea = "",
  user_aria_described_by: str = "",
  value: str = "",
  readonly: bool = False,
  hide_required_marker: bool = False,
  color: Literal["primary", "accent", "warn"] = "primary",
  float_label: Literal["always", "auto"] = "auto",
  appearance: Literal["fill", "outline"] = "fill",
  subscript_sizing: Literal["fixed", "dynamic"] = "fixed",
  hint_label: str = "",
  label: str = "",
  style: str = "",
  on_input: Callable[[InputEvent], Any] | None = None,
):
  """Creates a Input component.

  Args:
    key: Unique identifier for this component instance.
    disabled: Implemented as part of MatFormFieldControl. @docs-private
    id: Implemented as part of MatFormFieldControl. @docs-private
    placeholder: Implemented as part of MatFormFieldControl. @docs-private
    name: Name of the input. @docs-private
    required: Implemented as part of MatFormFieldControl. @docs-private
    type: Input type of the element. For textarea, use `me.Textarea(...)`
    user_aria_described_by: Implemented as part of MatFormFieldControl. @docs-private
    value: Implemented as part of MatFormFieldControl. @docs-private
    readonly: Whether the element is readonly.
    hide_required_marker: Whether the required marker should be hidden.
    color: The color palette for the form field.
    float_label: Whether the label should always float or float as the user types.
    appearance: The form field appearance style.
    subscript_sizing: Whether the form field should reserve space for one line of hint/error text (default) or to have the spacing grow from 0px as needed based on the size of the hint/error content. Note that when using dynamic sizing, layout shifts will occur when hint/error text changes.
    hint_label: Text for the form field hint.
    label: Label for input.
    style: Style for input.
    on_input: [input](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/input_event) is a native browser event.
  """
  textarea = None
  if isinstance(type, Textarea):
    textarea = type
    type_string = "textarea"
  else:
    type_string = cast(str, type)
  insert_component(
    key=key,
    type_name="input",
    proto=input_pb.InputType(
      textarea_rows=textarea.rows if textarea else 0,
      disabled=disabled,
      id=id,
      placeholder=placeholder,
      name=name,
      required=required,
      type=type_string,
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
      style=style,
      on_input_handler_id=register_event_handler(on_input, event=InputEvent)
      if on_input
      else "",
    ),
  )
