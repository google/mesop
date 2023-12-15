import os.path

from absl import app, flags

import component_specs.component_spec_pb2 as pb
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
CHECKBOX_SPEC = pb.ComponentSpec()


def main(argv):
  name = CHECKBOX_SPEC.input.name
  if FLAGS.write:
    write(
      generate_ng_template(CHECKBOX_SPEC),
      name,
      ext="ng.html",
    )
    write(
      generate_ng_ts(CHECKBOX_SPEC),
      name,
      ext="ts",
    )
    write(
      generate_proto_schema(CHECKBOX_SPEC),
      name,
      ext="proto",
    )
    write(
      generate_py_component(CHECKBOX_SPEC),
      name,
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


if __name__ == "__main__":
  app.run(main)
