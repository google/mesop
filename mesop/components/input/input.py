from dataclasses import dataclass
from typing import Any, Callable, Literal, cast

import mesop.components.input.input_pb2 as input_pb
from mesop.component_helpers import (
  Style,
  insert_component,
  register_event_handler,
  to_style_proto,
)
from mesop.events import InputEvent
from mesop.utils.validate import validate


@dataclass
class Textarea:
  """
  Represents a multi-line text input control.

  Attributes:
      rows: The number of lines to show in the text area.
  """

  rows: int = 5


@validate
def input(
  *,
  label: str = "",
  on_input: Callable[[InputEvent], Any] | None = None,
  type: Literal[
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
  | Textarea
  | None = None,
  appearance: Literal["fill", "outline"] = "fill",
  style: Style | None = None,
  disabled: bool = False,
  placeholder: str = "",
  name: str = "",
  required: bool = False,
  value: str = "",
  readonly: bool = False,
  hide_required_marker: bool = False,
  color: Literal["primary", "accent", "warn"] = "primary",
  float_label: Literal["always", "auto"] = "auto",
  subscript_sizing: Literal["fixed", "dynamic"] = "fixed",
  hint_label: str = "",
  key: str | None = None,
):
  """Creates a Input component.

  Args:
    label: Label for input.
    on_input: [input](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/input_event) is a native browser event.
    type: Input type of the element. For textarea, use `me.Textarea(...)`
    appearance: The form field appearance style.
    style: Style for input.
    disabled: Whether it's disabled.
    placeholder: Placeholder value
    name: Name of the input.
    required: Whether it's required
    value: Initial value.
    readonly: Whether the element is readonly.
    hide_required_marker: Whether the required marker should be hidden.
    color: The color palette for the form field.
    float_label: Whether the label should always float or float as the user types.
    subscript_sizing: Whether the form field should reserve space for one line of hint/error text (default) or to have the spacing grow from 0px as needed based on the size of the hint/error content. Note that when using dynamic sizing, layout shifts will occur when hint/error text changes.
    hint_label: Text for the form field hint.
    key: Unique identifier for this component instance.
  """
  textarea = None
  if isinstance(type, Textarea):
    textarea = type
    type_string = "textarea"
  elif type is None:
    type_string = ""
  else:
    type_string = cast(str, type)
  insert_component(
    key=key,
    type_name="input",
    proto=input_pb.InputType(
      textarea_rows=textarea.rows if textarea else 0,
      disabled=disabled,
      placeholder=placeholder,
      name=name,
      required=required,
      type=type_string,
      value=value,
      readonly=readonly,
      hide_required_marker=hide_required_marker,
      color=color,
      float_label=float_label,
      appearance=appearance,
      subscript_sizing=subscript_sizing,
      hint_label=hint_label,
      label=label,
      on_input_handler_id=register_event_handler(on_input, event=InputEvent)
      if on_input
      else "",
    ),
    style=to_style_proto(style) if style else None,
  )
