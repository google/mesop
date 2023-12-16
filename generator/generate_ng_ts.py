import generator.component_spec_pb2 as pb
from generator.format_types import format_proto_xtype
from generator.utils import (
  capitalize_first_letter,
  get_path_from_workspace_root,
  upper_camel_case,
)


def generate_ng_ts(spec: pb.ComponentSpec) -> str:
  file_path = get_path_from_workspace_root(
    "generator", "fixtures", "component_name.ts"
  )
  with open(
    file_path,
  ) as f:
    ts_template = f.read()

  # default_value_prop = [
  #   prop for prop in spec.input_props if prop.name == "value"
  # ][0]
  for ng_module in spec.input.ng_modules:
    symbols = ",".join([ng_module.module_name] + list(ng_module.other_symbols))
    symbols = "{" + symbols + "}"

    ts_template = (
      f"import {symbols} from '{ng_module.import_path}'\n" + ts_template
    )
  # Do simple string replacements
  ts_template = (
    ts_template.replace("component_name", spec.input.name)
    .replace("ComponentName", upper_camel_case(spec.input.name))
    .replace("// INSERT_EVENT_METHODS:", generate_ts_methods(spec))
    .replace("// GENERATE_NG_IMPORTS:", generate_ng_imports(spec))
  )

  return ts_template


def generate_ng_imports(spec: pb.ComponentSpec) -> str:
  return f"imports: [{','.join([ng_module.module_name for ng_module in spec.input.ng_modules])}]"


def generate_ts_methods(spec: pb.ComponentSpec) -> str:
  out = ""
  for input_prop in spec.input_props:
    out += generate_ts_getter_method(input_prop)
  for prop in spec.output_props:
    out += generate_ts_event_method(prop)
  for native_event in spec.input.native_events:
    out += generate_ts_native_event_method(native_event)
  return out


def generate_ts_getter_method(prop: pb.Prop) -> str:
  string_literals = list(prop.type.string_literals.string_literal)
  type = "|".join(["'" + literal + "'" for literal in string_literals])
  capitalized_name = capitalize_first_letter(prop.name)
  if string_literals:
    return f"""
    get{capitalized_name}(): {type} {{
      return this.config().get{capitalized_name}() as {type};
    }}
    """
  return ""


def generate_ts_event_method(prop: pb.OutputProp) -> str:
  arg = (
    "event"
    if prop.event_js_type.is_primitive
    else f"event.{prop.event_props[0].name}"
  )
  return f"""
  on{prop.event_name}(event: {prop.event_js_type.type_name}): void {{
    const userEvent = new UserEvent();
    userEvent.set{format_proto_xtype(prop.event_props[0].type).capitalize()}({arg})
    userEvent.setHandlerId(this.config().getOn{prop.event_name}HandlerId())
    userEvent.setKey(this.key);
    this.channel.dispatch(userEvent);
  }}
  """


def generate_ts_native_event_method(native_event: str) -> str:
  native_event_name = upper_camel_case(native_event)
  if native_event == "input":
    return f"""
  on{native_event_name}(event: Event): void {{
    const userEvent = new UserEvent();
    userEvent.setHandlerId(this.config().getOn{native_event_name}HandlerId())
    userEvent.setString((event.target as HTMLInputElement).value);
    userEvent.setKey(this.key);
    this.channel.dispatch(userEvent);
  }}
  """

  return f"""
  on{native_event_name}(event: Event): void {{
    const userEvent = new UserEvent();
    userEvent.setHandlerId(this.config().getOn{native_event_name}HandlerId())
    userEvent.setKey(this.key);
    this.channel.dispatch(userEvent);
  }}
  """
