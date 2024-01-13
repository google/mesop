from typing import Any, Callable, Literal

import mesop.components.input.input_pb2 as input_pb
from mesop.component_helpers import (
  Style,
  insert_component,
  register_event_handler,
  register_native_component,
  to_style_proto,
)
from mesop.events import InputEvent


@register_native_component
def textarea(
  *,
  label: str = "",
  on_input: Callable[[InputEvent], Any] | None = None,
  rows: int = 5,
  appearance: Literal["fill", "outline"] = "fill",
  style: Style | None = None,
  disabled: bool = False,
  placeholder: str = "",
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
  """Creates a Textarea component.

  Args:
    label: Label for input.
    on_input: [input](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/input_event) is a native browser event.
    rows: The number of lines to show in the text area.
    appearance: The form field appearance style.
    style: Style for input.
    disabled: Whether it's disabled.
    placeholder: Placeholder value
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

  insert_component(
    key=key,
    type_name="textarea",
    proto=input_pb.InputType(
      is_textarea=True,
      disabled=disabled,
      placeholder=placeholder,
      required=required,
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


@register_native_component
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
  | None = None,
  appearance: Literal["fill", "outline"] = "fill",
  style: Style | None = None,
  disabled: bool = False,
  placeholder: str = "",
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

  insert_component(
    key=key,
    type_name="input",
    proto=input_pb.InputType(
      is_textarea=False,
      disabled=disabled,
      placeholder=placeholder,
      required=required,
      type=type,
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
