import collections.abc
import inspect
from dataclasses import is_dataclass
from types import NoneType
from typing import Any, Callable, ItemsView, Literal, Sequence

import mesop.protos.ui_pb2 as pb
from mesop.components.badge.badge import badge
from mesop.components.box.box import box
from mesop.components.button.button import button
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
    generate_component_config(button),
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
    fields=get_fields(sig.parameters.items()),
  )
  return component_config


def get_fields(
  items: ItemsView[str, inspect.Parameter],
) -> list[pb.EditorField]:
  fields: list[pb.EditorField] = []
  for name, param in items:
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
    elif param_type is float:
      field_type = pb.FieldType(float_type=pb.FloatType(default_value=0))
    elif param_type is str or (
      # special case, for int|str (used for styles, e.g. pixel value), use str
      args and len(args) == 2 and args[0] is int and args[1] is str
    ):
      field_type = pb.FieldType(string_type=pb.StringType())
    elif getattr(param_type, "__origin__", None) is Literal:
      field_type = pb.FieldType(
        literal_type=pb.LiteralType(literals=map_literals(param_type.__args__))
      )
    elif getattr(param_type, "__origin__", None) is list:
      el_fields = get_fields(
        inspect.signature(param_type.__args__[0]).parameters.items()
      )
      field_type = pb.FieldType(
        list_type=pb.ListType(
          type=pb.FieldType(struct_type=pb.StructType(fields=el_fields))
        )
      )
    elif is_dataclass(param_type):
      param_items = inspect.signature(param_type).parameters.items()
      el_fields = get_fields(param_items)

      field_type = pb.FieldType(struct_type=pb.StructType(fields=el_fields))
    elif isinstance(param_type, collections.abc.Callable):
      field_type = None
    else:
      raise MesopInternalException(
        "Unhandled param type", param_type, "field_name", name
      )

    fields.append(pb.EditorField(name=name, type=field_type))

  return fields


def map_literals(literals: Sequence[int | str]) -> list[pb.LiteralElement]:
  out: list[pb.LiteralElement] = []
  for literal in literals:
    if isinstance(literal, str):
      out.append(pb.LiteralElement(string_literal=literal))
    elif isinstance(literal, int):  # type: ignore
      out.append(pb.LiteralElement(int_literal=literal))
    else:
      raise MesopInternalException("Unhandled literal case", literal)

  return out
