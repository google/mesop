import os.path

from absl import app, flags

import generator.component_spec_pb2 as pb
from generator.generate_ng_template import generate_ng_template
from generator.generate_ng_ts import generate_ng_ts
from generator.generate_proto_schema import generate_proto_schema
from generator.generate_py_component import generate_py_component
from generator.utils import (
  get_bazel_workspace_directory,
)

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

flags.DEFINE_bool("write", False, "set to true to write files.")
flags.DEFINE_string("component", "", "name of component (snake_case).")


def main(argv):
  pb_path = os.path.join(
    get_bazel_workspace_directory(),
    "generator",
    "output_data",
    f"{FLAGS.component}.binarypb",
  )
  spec = pb.ComponentSpec()
  with open(pb_path, "rb") as f:
    spec.ParseFromString(f.read())

  name = spec.input.name
  write(generate_ng_template(spec), name, ext="ng.html")
  write(generate_ng_ts(spec), name, ext="ts")
  write(generate_proto_schema(spec), name, ext="proto")
  write(generate_py_component(spec), name, ext="py")
  if FLAGS.write:
    print("Written files")


def write(contents: str, name: str, ext: str):
  if FLAGS.write:
    with open(
      os.path.join(
        get_bazel_workspace_directory(), f"mesop/components/{name}/{name}.{ext}"
      ),
      "w",
    ) as f:
      f.write(contents)
  else:
    print(f"Dry run for {name}.{ext}:", contents)


if __name__ == "__main__":
  app.run(main)
