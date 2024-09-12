from dataclasses import dataclass
from typing import Any, Callable, Iterable, Literal

import mesop.components.autocomplete.autocomplete_pb2 as autocomplete_pb
from mesop.component_helpers import (
  Style,
  insert_component,
  register_event_handler,
  register_event_mapper,
  register_native_component,
)
from mesop.events import InputEvent, MesopEvent


@dataclass(kw_only=True)
class AutocompleteOption:
  """
  Represents an option in the autocomplete drop down.

  Attributes:
    label: Content to show for the autocomplete option
    value: The value of this autocomplete option.
  """

  label: str | None = None
  value: str | None = None


@dataclass(kw_only=True)
class AutocompleteOptionGroup:
  """
  Represents an option group to group options in the autocomplete drop down.

  Attributes:
    label: Group label
    options: Autocomplete options under this group
  """

  label: str
  options: list[AutocompleteOption]


@dataclass(kw_only=True)
class AutocompleteEnterEvent(MesopEvent):
  """Represents an "Enter" keyboard event on an autocomplete component.

  Attributes:
    value: Input/selected value.
    key (str): key of the component that emitted this event.
  """

  value: str


register_event_mapper(
  AutocompleteEnterEvent,
  lambda event, key: AutocompleteEnterEvent(
    key=key.key,
    value=event.string_value,
  ),
)


@dataclass(kw_only=True)
class AutocompleteSelectionChangeEvent(MesopEvent):
  """Represents a selection change event.

  Attributes:
      value: Selected value.
      key (str): key of the component that emitted this event.
  """

  value: str


register_event_mapper(
  AutocompleteSelectionChangeEvent,
  lambda userEvent, key: AutocompleteSelectionChangeEvent(
    value=userEvent.string_value,
    key=key.key,
  ),
)


@register_native_component
def autocomplete(
  *,
  options: Iterable[AutocompleteOption | AutocompleteOptionGroup] | None = None,
  label: str = "",
  on_selection_change: Callable[[AutocompleteSelectionChangeEvent], Any]
  | None = None,
  on_input: Callable[[InputEvent], Any] | None = None,
  on_enter: Callable[[AutocompleteEnterEvent], Any] | None = None,
  appearance: Literal["fill", "outline"] = "fill",
  disabled: bool = False,
  placeholder: str = "",
  value: str = "",
  readonly: bool = False,
  hide_required_marker: bool = False,
  color: Literal["primary", "accent", "warn"] = "primary",
  float_label: Literal["always", "auto"] = "auto",
  subscript_sizing: Literal["fixed", "dynamic"] = "fixed",
  hint_label: str = "",
  style: Style | None = None,
  key: str | None = None,
):
  """Creates an autocomplete component.

  Args:
    options: Selectable options from autocomplete.
    label: Label for input.
    on_selection_change: Event emitted when the selected value has been changed by the user.
    on_input: [input](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/input_event) is fired whenever the input has changed (e.g. user types).
    on_enter: triggers when the browser detects an "Enter" key on a [keyup](https://developer.mozilla.org/en-US/docs/Web/API/Element/keyup_event) native browser event.
    appearance: The form field appearance style.
    disabled: Whether it's disabled.
    placeholder: Placeholder value.
    value: Initial value.
    readonly: Whether the element is readonly.
    hide_required_marker: Whether the required marker should be hidden.
    color: The color palette for the form field.
    float_label: Whether the label should always float or float as the user types.
    subscript_sizing: Whether the form field should reserve space for one line of hint/error text (default) or to have the spacing grow from 0px as needed based on the size of the hint/error content. Note that when using dynamic sizing, layout shifts will occur when hint/error text changes.
    hint_label: Text for the form field hint.
    style: Style for input.
    key: The component [key](../components/index.md#component-key).
  """

  insert_component(
    key=key,
    type_name="autocomplete",
    proto=autocomplete_pb.AutocompleteType(
      options=_make_autocomplete_options(options),
      disabled=disabled,
      placeholder=placeholder,
      value=value,
      readonly=readonly,
      hide_required_marker=hide_required_marker,
      color=color,
      float_label=float_label,
      appearance=appearance,
      subscript_sizing=subscript_sizing,
      hint_label=hint_label,
      label=label,
      on_selection_change_handler_id=register_event_handler(
        on_selection_change, event=AutocompleteSelectionChangeEvent
      )
      if on_selection_change
      else "",
      on_input_handler_id=register_event_handler(on_input, event=InputEvent)
      if on_input
      else "",
      on_enter_handler_id=register_event_handler(
        on_enter, event=AutocompleteEnterEvent
      )
      if on_enter
      else "",
    ),
    style=style,
  )


def _make_autocomplete_options(
  options: Iterable[AutocompleteOption | AutocompleteOptionGroup] | None = None,
) -> list[autocomplete_pb.AutocompleteOptionSet]:
  """Converts AutocompleteOption/AutocompleteOptionGroup list to protos."""
  if not options:
    return []

  proto_options = []
  for option in options:
    if isinstance(option, AutocompleteOptionGroup):
      proto_options.append(
        autocomplete_pb.AutocompleteOptionSet(
          option_group=autocomplete_pb.AutocompleteOptionGroup(
            label=option.label,
            options=[
              autocomplete_pb.AutocompleteOption(
                label=sub_option.label, value=sub_option.value
              )
              for sub_option in option.options
            ],
          )
        )
      )
    else:
      proto_options.append(
        autocomplete_pb.AutocompleteOptionSet(
          option=autocomplete_pb.AutocompleteOption(
            label=option.label,
            value=option.value,
          )
        )
      )
  return proto_options
