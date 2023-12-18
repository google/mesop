from typing import Any

import generator.component_spec_pb2 as pb
from generator.format_types import format_proto_xtype
from generator.utils import (
  capitalize_first_letter,
  get_path_from_workspace_root,
  snake_case,
  upper_camel_case,
  wrap_quote,
)


def generate_py_component(spec: pb.ComponentSpec) -> str:
  file_path = get_path_from_workspace_root(
    "generator", "fixtures", "component_name.py"
  )
  with open(file_path) as f:
    py_template = f.read()
  py_template = (
    py_template.replace("component_name", spec.input.name)
    .replace("ComponentName", upper_camel_case(spec.input.name))
    .replace("# INSERT_EVENTS", generate_py_events(spec))
    .replace("# INSERT_COMPONENT_PARAMS", generate_py_component_params(spec))
    .replace("# INSERT_PROTO_CALLSITE", generate_py_proto_callsite(spec))
    .replace("# INSERT_COMPONENT_CALL", generate_py_callsite(spec))
    .replace("# INSERT_VARIANT_INDEX_FN", generate_index_variant_fn(spec))
    .replace("INSERT_DOC_STRING", generate_doc_string(spec))
  )

  return py_template


NEW_LINE = "\n"


def generate_doc_string(spec: pb.ComponentSpec):
  component_name = " ".join(capitalize_first_letter(spec.input.name).split("_"))
  composite_comment = ""
  if spec.input.has_content:
    composite_comment = f"{component_name} is a composite component.\n"
  PADDING = "    "
  out: list[str] = [
    PADDING + "key (str|None): Unique identifier for this component instance."
  ]
  for prop in spec.input_props:
    out.append(
      f"{snake_case(prop.name)} ({format_py_xtype(prop.type)}): {prop.docs}"
    )
  for prop in spec.output_props:
    out.append(
      f"on_{format_event_name(prop.event_name, spec)} (Callable[[{prop.event_name}], Any]|None): {prop.docs}"
    )
  for native_event in spec.input.native_events:
    out.append(
      f"on_{native_event} (Callable[[{format_native_event_name(native_event)}], Any]|None): [{native_event}](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/{native_event}_event) is a native browser event."
    )
  if len(spec.input.directive_names):
    out.append(
      f"variant ({format_string_literals(list(spec.input.directive_names))}): component variations"
    )
  return f"""Creates a {component_name} component.
  {composite_comment}
  Args:
{f"{NEW_LINE}{PADDING}".join(out)}"""


def generate_py_callsite(spec: pb.ComponentSpec):
  if spec.input.has_content:
    return "return insert_composite_component("
  return "insert_component("


def generate_py_events(spec: pb.ComponentSpec) -> str:
  out: list[str] = []
  for prop in spec.output_props:
    out.append(generate_py_event(prop))
  return "\n".join(out)


def generate_py_event(output_prop: pb.OutputProp) -> str:
  if len(output_prop.event_props):
    return f"""
@dataclass
class {output_prop.event_name}(MesopEvent):
  {output_prop.event_props[0].name}: {format_py_xtype(output_prop.event_props[0].type)}

register_event_mapper(
  {output_prop.event_name},
  lambda event, key: {output_prop.event_name}(
    key=key,
    {output_prop.event_props[0].name}=event.{format_proto_xtype(output_prop.event_props[0].type)},
  ),
)
    """
  return f"""
@dataclass
class {output_prop.event_name}(MesopEvent):
  pass

register_event_mapper(
  {output_prop.event_name},
  lambda event, key: {output_prop.event_name}(
    key=key,
  ),
)
  """


def generate_py_component_params(spec: pb.ComponentSpec) -> str:
  out: list[str] = ["key: str | None = None"]
  for prop in spec.input_props:
    out.append(
      f"{snake_case(prop.name)}: {format_py_xtype(prop.type)}={format_py_default_value_xtype(prop.type)}"
    )
  for prop in spec.output_props:
    out.append(
      f"on_{format_event_name(prop.event_name, spec)}: Callable[[{prop.event_name}], Any]|None=None"
    )
  for native_event in spec.input.native_events:
    out.append(
      f"on_{native_event}: Callable[[{format_native_event_name(native_event)}], Any]|None=None"
    )
  if len(spec.input.directive_names):
    out.append(
      f"variant: {format_string_literals(list(spec.input.directive_names))} = {wrap_quote(spec.input.directive_names[0])}"
    )
  return ", ".join(out)


def generate_py_proto_callsite(spec: pb.ComponentSpec) -> str:
  out: list[str] = []
  for prop in spec.input_props:
    out.append(f"{snake_case(prop.name)}={snake_case(prop.name)}")
  for prop in spec.output_props:
    event_name = format_event_name(prop.event_name, spec)
    event_param_name = f"on_{event_name}"
    out.append(
      f"on_{snake_case(prop.event_name)}_handler_id=register_event_handler({event_param_name}, event={prop.event_name}) if {event_param_name} else ''"
    )
  for native_event in spec.input.native_events:
    event_param_name = f"on_{native_event}"
    out.append(
      f"on_{native_event}_handler_id=register_event_handler({event_param_name}, event={format_native_event_name(native_event)}) if {event_param_name} else ''"
    )
  if len(spec.input.directive_names):
    out.append("variant_index=_get_variant_index(variant)")
  return ", ".join(out)


def generate_index_variant_fn(spec: pb.ComponentSpec) -> str:
  if not len(spec.input.directive_names):
    return ""

  exprs: list[str] = []
  for index, variant in enumerate(spec.input.directive_names):
    s = f"""
  if variant == '{variant}':
    return {index}"""
    exprs.append(s)
  return f"""
def _get_variant_index(variant: str) -> int:
  {''.join(exprs)}
  raise Exception("Unexpected variant: " + variant)
  """


def format_native_event_name(name: str) -> str:
  return upper_camel_case(name) + "Event"


def format_event_name(name: str, spec: pb.ComponentSpec) -> str:
  component_name = upper_camel_case(spec.input.name)
  event_name = name
  if name.startswith(component_name):
    event_name = name[len(component_name) :]
  if event_name.endswith("Event"):
    event_name = event_name[: len("Event") * -1]
  return snake_case(event_name)


def format_py_default_value_xtype(
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


def format_py_xtype(type: pb.XType) -> str:
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
    return format_string_literals(list(type.string_literals.string_literal))
  else:
    raise Exception("not yet handled", type)


def format_string_literals(literals: list[str]) -> str:
  literal_type = ",".join([wrap_quote(literal) for literal in literals])
  return f"Literal[{literal_type}]"
