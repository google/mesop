from typing import Any

import component_specs.component_spec_pb2 as pb
from component_specs.utils import wrap_quote


def format_type_ts(type: pb.XType) -> str:
  if type.simple_type:
    return format_js_type(type.simple_type)
  return "|".join(
    [f"'{literal}'" for literal in type.string_literals.string_literal]
  )


def format_type_for_python(type: pb.XType) -> str:
  if type.simple_type:
    if type.simple_type == pb.SimpleType.BOOL:
      return "bool"
    elif type.simple_type == pb.SimpleType.STRING:
      return "str"
    elif type.simple_type == pb.SimpleType.NUMBER:
      return "float"
    else:
      raise Exception("not yet handled", type)
  elif type.string_literals:
    literal_type = ",".join(
      [wrap_quote(literal) for literal in type.string_literals.string_literal]
    )
    return f"Literal[{literal_type}]"
  else:
    raise Exception("not yet handled", type)


def format_js_type(type: pb.SimpleType.ValueType) -> str:
  if type == pb.SimpleType.BOOL:
    return "boolean"
  elif type == pb.SimpleType.STRING:
    return "string"
  else:
    raise Exception("not yet handled", type)


def format_js_type_for_python(type: pb.SimpleType.ValueType) -> str:
  if type == pb.SimpleType.BOOL:
    return "bool"
  elif type == pb.SimpleType.STRING:
    return "str"
  else:
    raise Exception("not yet handled", type)


def format_js_type_default_value_for_python(
  type: pb.XType,
) -> Any:
  if type.simple_type:
    if type.simple_type == pb.SimpleType.BOOL:
      return False
    elif type.simple_type == pb.SimpleType.STRING:
      return "''"
    elif type.simple_type == pb.SimpleType.NUMBER:
      return 0
    else:
      raise Exception("not yet handled", type)
  elif type.string_literals:
    return '"' + type.string_literals.default_value + '"'
  else:
    raise Exception("not yet handled", type)


def format_xtype_for_proto(type: pb.XType) -> str:
  if type.simple_type:
    if type.simple_type == pb.SimpleType.BOOL:
      return "bool"
    elif type.simple_type == pb.SimpleType.STRING:
      return "string"
    elif type.simple_type == pb.SimpleType.NUMBER:
      return "double"
    else:
      raise Exception("not yet handled", type)
  elif type.string_literals:
    return "string"  # protos doesn't support string literals
  else:
    raise Exception("not yet handled", type)
