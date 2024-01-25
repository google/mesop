import inspect

import mesop.protos.ui_pb2 as pb


def get_caller_source_code_location(
  levels: int = 1,
) -> pb.SourceCodeLocation | None:
  current_frame = inspect.currentframe()

  # Walk backwards
  current_level = levels
  while current_level > 0:
    assert current_frame
    current_frame = current_frame.f_back
    current_level -= 1

  # If there's no caller frame, return an empty SourceCodeLocation
  if current_frame is None:
    return pb.SourceCodeLocation()

  caller_info = inspect.getframeinfo(current_frame)

  # Get module from filepath
  splitted_file = caller_info.filename.split("runfiles/")
  # Can't always look up from runfiles (e.g. colab).
  if len(splitted_file) < 2:
    return None
  segments = splitted_file[1].split("/")
  segments[len(segments) - 1] = segments[len(segments) - 1][: len(".py") * -1]
  module = ".".join(segments)

  return pb.SourceCodeLocation(
    module=module,
    line=caller_info.lineno,
  )
