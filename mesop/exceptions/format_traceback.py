import linecache
import sys
import traceback

import mesop.protos.ui_pb2 as pb


def format_traceback(
  lines_before: int = 2, lines_after: int = 4
) -> pb.Traceback:
  # Clear the linecache, otherwise we will potentially show
  # stale code in the traceback which is confusing.
  linecache.clearcache()

  # Initialize an empty string to accumulate traceback information
  res = pb.Traceback(frames=[])

  # Capture the current exception's traceback
  _, _, exc_traceback = sys.exc_info()

  # Iterate through the stack trace
  for frame, lineno in traceback.walk_tb(exc_traceback):
    filename = frame.f_code.co_filename
    code_name = frame.f_code.co_name
    stack_frame = pb.StackFrame(
      filename=format_filename(filename),
      code_name=code_name,
      line_number=lineno,
      lines=[],
      is_app_code=is_app_code(filename),
    )

    start_line = max(1, lineno - lines_before)
    end_line = lineno + lines_after
    for i in range(start_line, end_line + 1):
      code = linecache.getline(filename, i).rstrip()
      if len(code) > 0:
        stack_frame.lines.append(
          pb.ContextLine(code=code, is_caller=i == lineno)
        )
    res.frames.append(stack_frame)

  return res


def format_filename(filename: str) -> str:
  if "/python3" in filename:
    filename = "/python3" + filename.split("/python3", 1)[1]
  if ".runfiles" in filename:
    filename = "/" + filename.split(".runfiles", 1)[1]
  return filename


def is_app_code(filename: str) -> bool:
  """Use a naive but effective heuristic for whether this is 'application' code."""
  for i in range(1, len(linecache.getlines(filename)) + 1):
    if "import mesop as me" in linecache.getline(filename, i):
      return True
  return False
