import mesop.protos.ui_pb2 as pb
from component_specs.generate_from_spec import (
  generate_ng_template,
  generate_ng_ts,
  generate_proto_schema,
  generate_py_component,
)

# //   <mat-checkbox [checked]="isChecked" (change)="handleCheckboxChange($event)">
# //   {{config().getLabel()}}
# // </mat-checkbox>
CHECKBOX_SPEC = pb.ComponentSpec(
  type_name="checkbox",
  element_name="mat-checkbox",
  props=[
    pb.ElementProp(
      key="checked",
      property_binding=pb.PropertyBinding(name="value", type=pb.JsType.STRING),
    ),  # TODO: need a special marker for value (default value)
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


if __name__ == "__main__":
  print(".ng.html:")
  print(generate_ng_template(CHECKBOX_SPEC))
  print(".ts:")
  print(generate_ng_ts(CHECKBOX_SPEC))
  print(".proto:")
  print(generate_proto_schema(CHECKBOX_SPEC))
  print(":.py:")
  print(generate_py_component(CHECKBOX_SPEC))
