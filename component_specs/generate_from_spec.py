import mesop.protos.ui_pb2 as pb

"""
Spec recipe:
1. Generate Angular template (done)
2. Generate Angular TS (done)
3. Generate proto (done)
4. Generate Python method (done)

TODOs:
- doesn't handle event with multiple properties
- have better naming for events (either explicit control, or implicitly strip out Mat)
"""


def generate_ng_template(spec: pb.ComponentSpec) -> str:
  element_props = [format_element_prop(prop) for prop in spec.props]
  opening_braces = "{{"
  closing_braces = "}}"

  return f"""<{spec.element_name} {" ".join(element_props)}>
  {opening_braces}config().get{upper_camel_case(spec.content.name)}(){closing_braces}
  </{spec.element_name}>
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

  default_value_prop = [
    prop for prop in spec.props if prop.property_binding.name == "value"
  ][0]

  # Do simple string replacements
  ts_template = (
    ts_template.replace("component_name", spec.type_name)
    .replace("ComponentName", upper_camel_case(spec.type_name))
    .replace(
      "value: any;",
      f"value: {format_js_type(default_value_prop.property_binding.type)};",
    )
    .replace("// INSERT_EVENT_METHODS:", generate_ts_event_methods(spec))
  )

  # Build event handlers
  for prop in spec.props:
    if prop.HasField("event_binding"):
      ts_template = ts_template.replace(
        f"on{prop.event_binding.event_name}",
        f"handle{prop.event_binding.event_name}",
      )

  return ts_template


def generate_proto_schema(spec: pb.ComponentSpec) -> str:
  fields: list[str] = []
  index = 0

  for prop in spec.props:
    index += 1
    if prop.HasField("property_binding"):
      fields.append(f"{prop.property_binding.name} = {index};")
    if prop.HasField("event_binding"):
      fields.append(
        f"on_{snake_case(prop.event_binding.event_name)}_handler_id = {index};"
      )
  if spec.HasField("content"):
    index += 1
    fields.append(f"{spec.content.name} = {index};")

  message_contents = (
    "{\n" + "\n".join(["  " + field for field in fields]) + "\n}"
  )

  return f"""
syntax = "proto3";

package mesop.components.{spec.type_name};

message {upper_camel_case(spec.type_name)}Type {message_contents}

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
    py_template.replace("component_name", spec.type_name)
    .replace("ComponentName", upper_camel_case(spec.type_name))
    .replace("# INSERT_EVENTS", generate_py_events(spec))
    .replace("# INSERT_COMPONENT_PARAMS", generate_py_component_params(spec))
    .replace("# INSERT_PROTO_CALLSITE", generate_py_proto_callsite(spec))
  )

  return py_template


def generate_py_events(spec: pb.ComponentSpec) -> str:
  out: list[str] = []
  for prop in spec.props:
    if prop.HasField("event_binding"):
      out.append(generate_py_event(prop.event_binding))
  return "\n".join(out)


def generate_py_event(event_binding: pb.EventBinding) -> str:
  return f"""
@dataclass
class {event_binding.event_name}Event(MesopEvent):
  {event_binding.props[0].key}: {format_js_type_for_python(event_binding.props[0].type)}

register_event_mapper(
  {event_binding.event_name}Event,
  lambda event, key: {event_binding.event_name}Event(
    key=key,
    {event_binding.props[0].key}=event.{format_js_type_for_python(event_binding.props[0].type)},
  ),
)
  """


def generate_py_component_params(spec: pb.ComponentSpec) -> str:
  out: list[str] = []
  for prop in spec.props:
    if prop.HasField("property_binding"):
      out.append(
        f"{prop.property_binding.name}: {format_js_type_for_python(prop.property_binding.type)}"
      )
    if prop.HasField("event_binding"):
      out.append(
        f"on_{snake_case(prop.event_binding.event_name)}: Callable[[{prop.event_binding.event_name}Event], Any]"
      )
  if spec.HasField("content"):
    out.append(
      f"{spec.content.name}: {format_js_type_for_python(spec.content.type)}"
    )
  return ", ".join(out)


def generate_py_proto_callsite(spec: pb.ComponentSpec) -> str:
  out: list[str] = []
  for prop in spec.props:
    if prop.HasField("property_binding"):
      out.append(f"{prop.property_binding.name}={prop.property_binding.name}")
    if prop.HasField("event_binding"):
      out.append(
        f"on_{snake_case(prop.event_binding.event_name)}_handler_id=handler_type(on_{snake_case(prop.event_binding.event_name)})"
      )
  if spec.HasField("content"):
    out.append(f"{spec.content.name}={spec.content.name}")
  return ", ".join(out)


def generate_ts_event_methods(spec: pb.ComponentSpec) -> str:
  out = ""
  for prop in spec.props:
    if prop.HasField("event_binding"):
      out += generate_ts_event_method(prop.event_binding)
  return out


def generate_ts_event_method(event_binding: pb.EventBinding) -> str:
  return f"""
  handle{event_binding.event_name}(event: {event_binding.event_name}): void {{
    const userEvent = new UserEvent();
    userEvent.set{format_js_type(event_binding.props[0].type).capitalize()}(event.{event_binding.props[0].key})
    userEvent.setHandlerId(this.config().getOn{event_binding.event_name}HandlerId())
    userEvent.setKey(this.key);
    this.channel.dispatch(userEvent);
  }}
  """


def format_js_type(type: pb.JsType.ValueType) -> str:
  if type == pb.JsType.BOOL:
    return "boolean"
  elif type == pb.JsType.STRING:
    return "string"
  else:
    raise Exception("not yet handled", type)


def format_js_type_for_python(type: pb.JsType.ValueType) -> str:
  if type == pb.JsType.BOOL:
    return "bool"
  elif type == pb.JsType.STRING:
    return "str"
  else:
    raise Exception("not yet handled", type)


def format_element_prop(prop: pb.ElementProp) -> str:
  if prop.HasField("event_binding"):
    return f"""({prop.key})="on{prop.event_binding.event_name}($event)\""""
  elif prop.HasField("property_binding"):
    return f'[{prop.key}]="{prop.property_binding.name}"'
  elif prop.HasField("model_binding"):
    raise Exception("not yet implemented model_binding")
  else:
    raise Exception("not yet handled", prop)


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
