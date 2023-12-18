import os

from absl import app, flags

import generator.component_spec_pb2 as pb
from generator.generate_ng_template import generate_ng_template
from generator.generate_ng_ts import generate_ng_ts
from generator.generate_proto_schema import generate_proto_schema
from generator.generate_py_component import generate_py_component
from generator.utils import get_path_from_workspace_root

"""
Generates from component spec the following:
1. Angular template (ng.html)
2. Angular TS
3. Proto schema (.proto)
4. Python component

TODOs:
- make it clear what the spelling (camel vs. snake_case)

MAYBEs:
- doesn't handle event with multiple properties
"""
LABEL_PROP = pb.Prop(
  name="label",
  type=pb.XType(simple_type=pb.SimpleType.STRING),
  target=pb.Target.TARGET_LABEL,
)

FLAGS = flags.FLAGS

flags.DEFINE_bool("dry_run", False, "set to true to write files.")


def main(argv):
  # Process all binarypb files in output_data dir
  output_data_path = get_path_from_workspace_root("generator", "output_data")
  form_field_spec = pb.ComponentSpec()
  form_field_path = os.path.join(output_data_path, "form_field.binarypb")
  with open(form_field_path, "rb") as f:
    form_field_spec.ParseFromString(f.read())
  for prop in form_field_spec.input_props:
    prop.target = pb.Target.TARGET_FORM_FIELD
  for file in os.listdir(output_data_path):
    full_path = os.path.join(output_data_path, file)
    if (
      os.path.isfile(full_path)
      and file.endswith(".binarypb")
      and not (
        file.endswith("form_field.binarypb")
        or file.endswith("radio.binarypb")
        or file.endswith("select.binarypb")
      )
    ):
      process_component(full_path, form_field_spec)


def process_component(pb_path: str, form_field_spec: pb.ComponentSpec):
  spec = pb.ComponentSpec()
  with open(pb_path, "rb") as f:
    spec.ParseFromString(f.read())

  if spec.input.is_form_field:
    spec.input_props.MergeFrom(form_field_spec.input_props)
    label_prop = pb.Prop()
    # Copy from constant just in case there's any unexpected proto mutations.
    label_prop.CopyFrom(LABEL_PROP)
    spec.input_props.append(label_prop)
  name = spec.input.name
  write(generate_ng_template(spec), name, ext="ng.html")
  write(generate_ng_ts(spec), name, ext="ts")
  write(generate_proto_schema(spec), name, ext="proto")
  write(generate_py_component(spec), name, ext="py")
  if not FLAGS.dry_run:
    print("Written files")


def write(contents: str, name: str, ext: str):
  if FLAGS.dry_run:
    print(f"Dry run for {name}.{ext}:", contents)
  else:
    with open(
      get_path_from_workspace_root(
        "mesop", "components", name, f"{name}.{ext}"
      ),
      "w",
    ) as f:
      f.write(contents)


if __name__ == "__main__":
  app.run(main)
