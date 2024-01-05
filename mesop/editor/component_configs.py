import mesop.protos.ui_pb2 as pb


def get_component_configs() -> list[pb.ComponentConfig]:
  return [
    pb.ComponentConfig(component_name="Box", category="Layout"),
    pb.ComponentConfig(component_name="Button", category="Form"),
  ]
