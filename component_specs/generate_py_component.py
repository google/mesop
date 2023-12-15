import component_specs.component_spec_pb2 as pb
from component_specs.format_types import (
  format_js_type_default_value_for_python,
  format_type_for_python,
  format_xtype_for_proto,
)
from component_specs.utils import (
  snake_case,
  upper_camel_case,
)


def generate_py_component(spec: pb.ComponentSpec) -> str:
  # TODO: should use runfiles
  with open(
    "/Users/will/Documents/GitHub/mesop/component_specs/fixtures/component_name.py",
  ) as f:
    py_template = f.read()
  py_template = (
    py_template.replace("component_name", spec.input.name)
    .replace("ComponentName", upper_camel_case(spec.input.name))
    .replace("# INSERT_EVENTS", generate_py_events(spec))
    .replace("# INSERT_COMPONENT_PARAMS", generate_py_component_params(spec))
    .replace("# INSERT_PROTO_CALLSITE", generate_py_proto_callsite(spec))
    .replace("# INSERT_COMPONENT_CALL", generate_py_callsite(spec))
  )

  return py_template


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
  return f"""
@dataclass
class {output_prop.event_name}(MesopEvent):
  {output_prop.event_props[0].name}: {format_type_for_python(output_prop.event_props[0].type)}

register_event_mapper(
  {output_prop.event_name},
  lambda event, key: {output_prop.event_name}(
    key=key,
    {output_prop.event_props[0].name}=event.{format_xtype_for_proto(output_prop.event_props[0].type)},
  ),
)
  """


def generate_py_component_params(spec: pb.ComponentSpec) -> str:
  out: list[str] = ["key: str | None = None"]
  for prop in spec.input_props:
    out.append(
      f"{snake_case(prop.name)}: {format_type_for_python(prop.type)}={format_js_type_default_value_for_python(prop.type)}"
    )
  for prop in spec.output_props:
    out.append(
      f"on_{format_event_name(prop.event_name, spec)}: Callable[[{prop.event_name}], Any]|None=None"
    )
  return ", ".join(out)


def generate_py_proto_callsite(spec: pb.ComponentSpec) -> str:
  out: list[str] = []
  for prop in spec.input_props:
    out.append(f"{snake_case(prop.name)}={snake_case(prop.name)}")
  for prop in spec.output_props:
    event_param_name = f"on_{format_event_name(prop.event_name, spec)}"
    out.append(
      f"on_{snake_case(prop.event_name)}_handler_id=handler_type({event_param_name}) if {event_param_name} else ''"
    )
  return ", ".join(out)


def format_event_name(name: str, spec: pb.ComponentSpec) -> str:
  component_name = upper_camel_case(spec.input.name)
  event_name = name
  if name.startswith(component_name):
    event_name = name[len(component_name) :]
  if event_name.endswith("Event"):
    event_name = event_name[: len("Event") * -1]
  return snake_case(event_name)
