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

FLAGS = flags.FLAGS

flags.DEFINE_bool("dry_run", False, "set to true to write files.")


def main(argv):
  # Process all binarypb files in output_data dir
  output_data_path = get_path_from_workspace_root("generator", "output_data")
  for file in os.listdir(output_data_path):
    full_path = os.path.join(output_data_path, file)
    if os.path.isfile(full_path) and file.endswith(".binarypb"):
      process_component(full_path)


def process_component(pb_path: str):
  spec = pb.ComponentSpec()
  with open(pb_path, "rb") as f:
    spec.ParseFromString(f.read())

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
