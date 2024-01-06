import mesop.protos.ui_pb2 as pb


def handle_editor_event(event: pb.EditorEvent):
  print("TODO_handle_editor_event", event)
  # Get into the Blaze working directory
  # Find the actual file from the module name
  # Get the correct target based on source code location
  # find the keyword argument
  # replace the value with this
  # update the file
  # this should trigger a hot reload event
  pass
