import os.path

from absl import app, flags

import mesop.protos.ui_pb2 as pb
from component_specs.generate_from_spec import (
  generate_ng_template,
  generate_ng_ts,
  generate_proto_schema,
  generate_py_component,
)

FLAGS = flags.FLAGS

flags.DEFINE_bool("write", False, "set to true to write files.")


# //   <mat-checkbox [checked]="isChecked" (change)="handleCheckboxChange($event)">
# //   {{config().getLabel()}}
# // </mat-checkbox>
CHECKBOX_SPEC = pb.ComponentSpec(
  type_name="checkbox",
  element_name="mat-checkbox",
  ng_module=pb.NgModuleSpec(
    import_path="@angular/material/checkbox",
    module_name="MatCheckboxModule",
    other_symbols=["MatCheckboxChange"],
  ),
  props=[
    pb.ElementProp(
      key="checked",
      property_binding=pb.PropertyBinding(name="value", type=pb.JsType.BOOL),
    ),  # TODO: need a special marker for value (default value)
    pb.ElementProp(
      key="change",
      event_binding=pb.EventBinding(
        event_name="MatCheckboxChange",
        props=[pb.EventProp(key="checked", type=pb.JsType.BOOL)],
      ),
    ),
  ],
  content=pb.ContentSpec(name="label", type=pb.JsType.STRING),
)


def main(argv):
  if FLAGS.write:
    write(
      generate_ng_template(CHECKBOX_SPEC),
      CHECKBOX_SPEC.type_name,
      ext="ng.html",
    )
    write(
      generate_ng_ts(CHECKBOX_SPEC),
      CHECKBOX_SPEC.type_name,
      ext="ts",
    )
    write(
      generate_proto_schema(CHECKBOX_SPEC),
      CHECKBOX_SPEC.type_name,
      ext="proto",
    )
    write(
      generate_py_component(CHECKBOX_SPEC),
      CHECKBOX_SPEC.type_name,
      ext="py",
    )

    print("Written files")
  else:
    print(".ng.html:")
    print(generate_ng_template(CHECKBOX_SPEC))
    print(".ts:")
    print(generate_ng_ts(CHECKBOX_SPEC))
    print(".proto:")
    print(generate_proto_schema(CHECKBOX_SPEC))
    print(":.py:")
    print(generate_py_component(CHECKBOX_SPEC))


def write(contents: str, name: str, ext: str):
  with open(
    os.path.join(
      get_bazel_workspace_directory(), f"mesop/components/{name}/{name}.{ext}"
    ),
    "w",
  ) as f:
    f.write(contents)


def get_bazel_workspace_directory() -> str:
  value = os.environ.get("BUILD_WORKSPACE_DIRECTORY")
  assert value
  return value


# workspace_dir = get_bazel_workspace_directory()
# print(f"Bazel workspace directory: {workspace_dir}")

if __name__ == "__main__":
  app.run(main)
