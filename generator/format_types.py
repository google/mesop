import generator.component_spec_pb2 as pb


def format_proto_xtype(type: pb.XType) -> str:
  if type.simple_type:
    if type.simple_type == pb.SimpleType.BOOL:
      return "bool"
    elif type.simple_type == pb.SimpleType.STRING:
      return "string"
    elif type.simple_type == pb.SimpleType.NUMBER:
      return "double"
    else:
      raise Exception("not yet handled", type)
  elif type.string_literals:
    return "string"  # protos doesn't support string literals
  else:
    raise Exception("not yet handled", type)
