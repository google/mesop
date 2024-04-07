import mesop.protos.ui_pb2 as pb
from mesop.runtime import runtime


def log_component_warning(message: str):
  runtime().add_warning(pb.Warning(message=message))
