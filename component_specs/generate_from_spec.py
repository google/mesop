from typing import Any

import component_specs.component_spec_pb2 as pb

"""
Generates from component spec the following:
1. Angular template (ng.html)
2. Angular TS
3. Proto schema (.proto)
4. Python component

TODOs:
- seperate out component spec protos into its own file
- make it clear what the spelling (camel vs. snake_case)

MAYBEs:
- doesn't handle event with multiple properties
- have better naming for events (either explicit control, or implicitly strip out Mat)
"""


def generate_ng_template(spec: pb.ComponentSpec) -> str:
  element_props = [format_input_prop(prop) for prop in spec.input_props] + [
    format_output_prop(prop) for prop in spec.output_props
  ]
  # TODO: implmeent content
  #   opening_braces = "{{"
  #   closing_braces = "}}"
  # {opening_braces}config().get{upper_camel_case(spec.content.name)}(){closing_braces}
  return f"""<{spec.input.element_name} {" ".join(element_props)}>

  </{spec.input.element_name}>
    """


def generate_ng_ts(spec: pb.ComponentSpec) -> str:
  """
  Read from component_name.ts
  Do simple string replacements
  Build event handlers
  """

  # TODO: should use runfiles
  with open(
    "/Users/will/Documents/GitHub/mesop/component_specs/fixtures/component_name.ts",
  ) as f:
    ts_template = f.read()

  # default_value_prop = [
  #   prop for prop in spec.input_props if prop.name == "value"
  # ][0]
  symbols = ",".join(
    [spec.input.ng_module.module_name]
    + list(spec.input.ng_module.other_symbols)
  )
  symbols = "{" + symbols + "}"

  ts_template = (
    f"import {symbols} from '{spec.input.ng_module.import_path}'\n"
    + ts_template
  )
  # Do simple string replacements
  ts_template = (
    ts_template.replace("component_name", spec.input.name)
    .replace("ComponentName", upper_camel_case(spec.input.name))
    # .replace(
    #   "value!: any;",
    #   f"value!: {format_type_ts(default_value_prop.type)};",
    # )
    .replace("// INSERT_EVENT_METHODS:", generate_ts_event_methods(spec))
    .replace("// GENERATE_NG_IMPORTS:", generate_ng_imports(spec))
  )

  return ts_template


def generate_ng_imports(spec: pb.ComponentSpec) -> str:
  return f"imports: [{spec.input.ng_module.module_name}]"


def generate_proto_schema(spec: pb.ComponentSpec) -> str:
  fields: list[str] = []
  index = 0

  for prop in spec.input_props:
    index += 1
    fields.append(f"{format_xtype_for_proto(prop.type)} {prop.name} = {index};")
  for prop in spec.output_props:
    if prop.HasField("event_binding"):
      fields.append(
        f"string on_{snake_case(prop.event_name)}_handler_id = {index};"
      )
  if spec.input.has_content:
    # TODO: create a wrapper-style component
    pass

  message_contents = (
    "{\n" + "\n".join(["  " + field for field in fields]) + "\n}"
  )

  return f"""
syntax = "proto3";

package mesop.components.{spec.input.name};

message {upper_camel_case(spec.input.name)}Type {message_contents}

  """


def generate_py_component(spec: pb.ComponentSpec) -> str:
  """
  Read from component_name.py
  Do simple string replacements
  Build event handlers
  """
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
  )

  return py_template


def generate_py_events(spec: pb.ComponentSpec) -> str:
  out: list[str] = []
  for prop in spec.output_props:
    out.append(generate_py_event(prop))
  return "\n".join(out)


def generate_py_event(output_prop: pb.OutputProp) -> str:
  return f"""
@dataclass
class {output_prop.event_name}Event(MesopEvent):
  {output_prop.event_props[0].name}: {format_type_for_python(output_prop.event_props[0].type)}

register_event_mapper(
  {output_prop.event_name}Event,
  lambda event, key: {output_prop.event_name}Event(
    key=key,
    {output_prop.event_props[0].name}=event.{format_xtype_for_proto(output_prop.event_props[0].type)},
  ),
)
  """


def generate_py_component_params(spec: pb.ComponentSpec) -> str:
  out: list[str] = ["key: str | None = None"]
  for prop in spec.input_props:
    out.append(
      f"{prop.name}: {format_type_for_python(prop.type)}={format_js_type_default_value_for_python(prop.type)}"
    )
  for prop in spec.output_props:
    out.append(
      f"on_{snake_case(prop.event_name)}: Callable[[{prop.event_name}Event], Any]|None=None"
    )
  return ", ".join(out)


def generate_py_proto_callsite(spec: pb.ComponentSpec) -> str:
  out: list[str] = []
  for prop in spec.input_props:
    out.append(f"{prop.name}={prop.name}")
  for prop in spec.output_props:
    out.append(
      f"on_{snake_case(prop.event_name)}_handler_id=handler_type(on_{snake_case(prop.event_name)}) if on_{snake_case(prop.event_name)} else ''"
    )
  return ", ".join(out)


def generate_ts_event_methods(spec: pb.ComponentSpec) -> str:
  out = ""
  for prop in spec.output_props:
    out += generate_ts_event_method(prop)
  return out


def generate_ts_event_method(prop: pb.OutputProp) -> str:
  return f"""
  on{prop.event_name}(event: {prop.event_name}): void {{
    const userEvent = new UserEvent();
    userEvent.set{format_xtype_for_proto(prop.event_props[0].type).capitalize()}(event.{prop.event_props[0].name})
    userEvent.setHandlerId(this.config().getOn{prop.event_name}HandlerId())
    userEvent.setKey(this.key);
    this.channel.dispatch(userEvent);
  }}
  """


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
    return f"Literal[{[  wrap_quote(literal) for literal in type.string_literals.string_literal]}]"
  else:
    raise Exception("not yet handled", type)


def wrap_quote(str: str) -> str:
  return f"'{str}'"


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
    return "''"
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


def format_input_prop(prop: pb.Prop) -> str:
  return f'[{prop.name}]="{prop.name}"'


def format_output_prop(prop: pb.OutputProp) -> str:
  return f"""({prop.name})="on{prop.event_name}($event)\""""


def upper_camel_case(str: str) -> str:
  """
  Split underscore and make it UpperCamelCase
  """
  return "".join(x.title() for x in str.split("_"))


def snake_case(str: str) -> str:
  """
  Split UpperCamelCase and make it snake_case
  """
  snake_str = [str[0].lower()]
  for char in str[1:]:
    if char.isupper():
      snake_str.append("_")
    snake_str.append(char.lower())
  return "".join(snake_str)
