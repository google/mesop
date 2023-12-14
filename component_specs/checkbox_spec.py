import mesop.protos.ui_pb2 as pb

# //   <mat-checkbox [checked]="isChecked" (change)="handleCheckboxChange($event)">
# //   {{config().getLabel()}}
# // </mat-checkbox>
CHECKBOX_SPEC = pb.ComponentSpec(
  type_name="checkbox",
  element_name="mat-checkbox",
  props=[
    # pb.ElementProp(key="checked", property_binding=""),
    pb.ElementProp(
      key="change",
      event_binding=pb.EventBinding(
        event_name="MatCheckboxChange",
        props=[pb.EventProp(key="changed", type=pb.JsType.BOOL)],
      ),
    ),
  ],
  content=pb.ContentSpec(name="label", type=pb.JsType.STRING),
)

"""
Spec recipe:
1. Generate Angular template
2. Generate Angular TS
3. Generate Python method
"""


def generate_ng_template(spec: pb.ComponentSpec) -> str:
  element_props = [format_element_prop(prop) for prop in spec.props]
  opening_braces = "{{"
  closing_braces = "}}"

  return f"""<{spec.element_name} {" ".join(element_props)}>
  {opening_braces}config().getLabel({spec.content.name}){closing_braces}
  </{spec.element_name}>
    """


def generate_ng_ts(spec: pb.ComponentSpec) -> str:
  """
  Read from component_name.ts
  Do simple string replacements
  Build event handlers
  """
  pass


def format_element_prop(prop: pb.ElementProp) -> str:
  if prop.HasField("event_binding"):
    return f"""({prop.key})="on{prop.event_binding.event_name}($event)\""""
  elif prop.HasField("property_binding"):
    raise Exception("not yet implemented property_binding")
  elif prop.HasField("model_binding"):
    raise Exception("not yet implemented model_binding")
  else:
    raise Exception("not yet handled", prop)


if __name__ == "__main__":
  out = generate_ng_template(CHECKBOX_SPEC)
  print(out)
