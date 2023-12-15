import generator.component_spec_pb2 as pb
from generator.format_types import format_xtype_for_proto
from generator.utils import (
  snake_case,
  upper_camel_case,
)


def generate_proto_schema(spec: pb.ComponentSpec) -> str:
  fields: list[str] = []
  index = 0

  for prop in spec.input_props:
    index += 1
    fields.append(
      f"{format_xtype_for_proto(prop.type)} {snake_case(prop.name)} = {index};"
    )
  for prop in spec.output_props:
    index += 1
    fields.append(
      f"string on_{snake_case(prop.event_name)}_handler_id = {index};"
    )

  message_contents = (
    "{\n" + "\n".join(["  " + field for field in fields]) + "\n}"
  )

  return f"""
syntax = "proto3";

package mesop.components.{spec.input.name};

message {upper_camel_case(spec.input.name)}Type {message_contents}

  """
