import collections.abc
import inspect
from dataclasses import is_dataclass
from types import NoneType
from typing import Any, Callable, ItemsView, Literal, Sequence

import mesop.protos.ui_pb2 as pb
from mesop.exceptions import MesopInternalException
from mesop.runtime import runtime


def get_component_configs() -> list[pb.ComponentConfig]:
  return [
    generate_component_config(component)
    for component in runtime().get_component_fns()
  ]


def generate_component_config(fn: Callable[..., Any]) -> pb.ComponentConfig:
  sig = inspect.signature(fn)
  if "mesop.components." in fn.__module__:
    component_name = pb.ComponentName(
      core_module=True,
      fn_name=fn.__name__,
    )
  else:
    component_name = pb.ComponentName(
      module_path=fn.__module__,
      fn_name=fn.__name__,
    )

  component_config = pb.ComponentConfig(
    component_name=component_name,
    category="Default",
    fields=get_fields(sig.parameters.items()),
    accepts_child=sig.return_annotation is not inspect.Signature.empty,
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
    elif param_type is int:
      field_type = pb.FieldType(int_type=pb.IntType(default_value=0))
    elif param_type is float:
      field_type = pb.FieldType(float_type=pb.FloatType(default_value=0))
    elif (
      param_type is str
      or (
        # special case, for int|str|None (used for styles, e.g. pixel value), use str
        args
        and len(args) == 3
        and args[0] is int
        and args[1] is str
        and args[2] is NoneType
      )
      or (
        # special case, for float|str|None (used for styles, e.g. opacity), use str
        args
        and len(args) == 3
        and args[0] is float
        and args[1] is str
        and args[2] is NoneType
      )
    ):
      field_type = pb.FieldType(string_type=pb.StringType())
    elif getattr(param_type, "__origin__", None) is Literal:
      field_type = pb.FieldType(
        literal_type=pb.LiteralType(literals=map_literals(param_type.__args__))
      )
    elif getattr(param_type, "__origin__", None) is collections.abc.Iterable:
      cls = param_type.__args__[0]
      el_fields = get_fields(inspect.signature(cls).parameters.items())
      field_type = pb.FieldType(
        list_type=pb.ListType(
          type=pb.FieldType(
            struct_type=pb.StructType(
              struct_name=cls.__name__, fields=el_fields
            )
          )
        )
      )
    elif is_dataclass(param_type):
      param_items = inspect.signature(param_type).parameters.items()
      el_fields = get_fields(param_items)

      field_type = pb.FieldType(
        struct_type=pb.StructType(
          struct_name=param_type.__name__, fields=el_fields
        )
      )
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
