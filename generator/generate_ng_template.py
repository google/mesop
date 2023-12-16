import generator.component_spec_pb2 as pb
from generator.utils import capitalize_first_letter, upper_camel_case

# Void elements like <input> should not and cannot be closed (Angular compiler will complain)
SKIP_CLOSING_TAGS = ["input"]


def generate_ng_template(spec: pb.ComponentSpec) -> str:
  element_props = (
    [
      format_input_prop(prop)
      for prop in spec.input_props
      if prop.target == pb.Target.TARGET_UNDEFINED
    ]
    + [format_output_prop(prop) for prop in spec.output_props]
    + [
      format_native_event(native_event)
      for native_event in spec.input.native_events
    ]
  )
  closing_tag = (
    ""
    if spec.input.element_name in SKIP_CLOSING_TAGS
    else f"</{spec.input.element_name}>"
  )

  content = ""
  if spec.input.has_content:
    content = "<ng-content></ng-content>"

  def template(directive: str = "") -> str:
    out = f"""<{spec.input.element_name} {directive} {" ".join(element_props)}>
    {content}
  {closing_tag}
  """
    form_field_props = [
      format_input_prop(prop)
      for prop in spec.input_props
      if prop.target == pb.Target.TARGET_FORM_FIELD
    ]
    if spec.input.is_form_field:
      out = (
        f"<mat-form-field {' '.join(form_field_props)}>"
        # Hardcode label since it's a special case (assumed it's there when spec is form field)
        + "<mat-label>{{config().getLabel()}}</mat-label>"
        + out
        + "</mat-form-field>"
      )
    return out

  if not len(spec.input.directive_names):
    return template()
  # You cannot dynamically set the directive (e.g. for button class)
  # see: https://github.com/angular/components/issues/26350
  # As a workaround, we print the template N times where N = # of variants
  open_brace = "{"
  closed_brace = "}"
  outs: list[str] = []
  for index, directive in enumerate(spec.input.directive_names):
    outs.append(
      f"""
   @if(config().getVariantIndex() === {index}) {open_brace}
      {template(directive=directive)}
   {closed_brace}
   """
    )

  return "\n".join(outs)


def format_directives(spec: pb.ComponentSpec) -> str:
  if not len(spec.input.directive_names):
    return ""
  # assuming the first one is the default/main directive which can be overriden by the others
  # via attributes
  result = spec.input.directive_names[0]
  return (
    result
    + " "
    + "\n".join(
      [
        f"""[attr.{directive}]=\"config().getVariant() === '{directive}'\""""
        for directive in spec.input.directive_names
      ]
    )
  )


def format_input_prop(prop: pb.Prop) -> str:
  name = prop.alias if prop.alias else prop.name
  string_literals = list(prop.type.string_literals.string_literal)
  if string_literals:
    return f'[{name}]="get{capitalize_first_letter(prop.name)}()"'

  return f'[{name}]="config().get{capitalize_first_letter(prop.name)}()"'


def format_output_prop(prop: pb.OutputProp) -> str:
  return f"""({prop.name})="on{prop.event_name}($event)\""""


def format_native_event(native_event: str) -> str:
  return f"""({native_event})="on{upper_camel_case(native_event)}($event)\""""
