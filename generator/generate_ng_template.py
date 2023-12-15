import generator.component_spec_pb2 as pb
from generator.utils import (
  capitalize_first_letter,
)


def generate_ng_template(spec: pb.ComponentSpec) -> str:
  element_props = [format_input_prop(prop) for prop in spec.input_props] + [
    format_output_prop(prop) for prop in spec.output_props
  ]

  content = ""
  if spec.input.has_content:
    content = "<ng-content></ng-content>"
  return f"""<{spec.input.element_name} {" ".join(element_props)}>
    {content}
  </{spec.input.element_name}>
    """


def format_input_prop(prop: pb.Prop) -> str:
  name = prop.alias if prop.alias else prop.name
  string_literals = list(prop.type.string_literals.string_literal)
  if string_literals:
    return f'[{name}]="get{capitalize_first_letter(prop.name)}()"'

  return f'[{name}]="config().get{capitalize_first_letter(prop.name)}()"'


def format_output_prop(prop: pb.OutputProp) -> str:
  return f"""({prop.name})="on{prop.event_name}($event)\""""
