import collections.abc
import inspect
from types import NoneType
from typing import Any, Callable, Literal

import mesop.protos.ui_pb2 as pb
from mesop.components.badge.badge import badge
from mesop.components.box.box import box
from mesop.components.checkbox.checkbox import checkbox
from mesop.components.divider.divider import divider
from mesop.components.icon.icon import icon
from mesop.components.input.input import input
from mesop.components.markdown.markdown import markdown
from mesop.components.progress_bar.progress_bar import progress_bar
from mesop.components.progress_spinner.progress_spinner import progress_spinner
from mesop.components.radio.radio import radio
from mesop.components.select.select import select
from mesop.components.slide_toggle.slide_toggle import slide_toggle
from mesop.components.slider.slider import slider
from mesop.components.text.text import text
from mesop.components.tooltip.tooltip import tooltip
from mesop.exceptions import MesopInternalException


def get_component_configs() -> list[pb.ComponentConfig]:
  return [
    generate_component_config(badge),
    generate_component_config(box),
    generate_component_config(checkbox),
    generate_component_config(divider),
    generate_component_config(icon),
    generate_component_config(input),
    generate_component_config(markdown),
    generate_component_config(progress_bar),
    generate_component_config(progress_spinner),
    generate_component_config(radio),
    generate_component_config(select),
    generate_component_config(slider),
    generate_component_config(slide_toggle),
    generate_component_config(text),
    generate_component_config(tooltip),
  ]


def generate_component_config(fn: Callable[..., Any]) -> pb.ComponentConfig:
  sig = inspect.signature(fn)
  component_config = pb.ComponentConfig(
    component_name=fn.__name__,
    category="Default",
    fields=[],
  )

  for name, param in sig.parameters.items():
    editor_field = pb.EditorField(name=name, type=pb.FieldType())
    editor_field.name = name
    param_type = param.annotation

    # Unwrap optional:
    # e.g. str | none
    # e.g. Literal["a"] | None
    args = getattr(param_type, "__args__", None)
    if args and len(args) == 2 and args[1] is NoneType:
      param_type = param_type.__args__[0]

    # Map Python types to proto ParamType
    field_type = None
    if param_type is bool:
      field_type = pb.FieldType(bool_type=pb.BoolType(default_value=False))
    elif param_type is str:
      field_type = pb.FieldType(string_type=pb.StringType())
    elif getattr(param_type, "__origin__", None) is Literal:
      field_type = pb.FieldType(
        string_literal_type=pb.StringLiteralType(literals=param_type.__args__)
      )
    elif isinstance(param_type, collections.abc.Callable):
      field_type = None
    else:
      raise MesopInternalException(
        "Unhandled param type", param_type, "field_name", name
      )

    component_config.fields.append(pb.EditorField(name=name, type=field_type))

  return component_config
