import inspect
import os

import mesop.protos.ui_pb2 as pb


def get_app_caller_source_code_location() -> pb.SourceCodeLocation | None:
  current_frame = inspect.currentframe()

  while current_frame:
    caller_info = inspect.getframeinfo(current_frame)
    filename = caller_info.filename
    # "mesop/mesop" is the file path of the core Mesop framework when running under bazel.
    # The exception is the examples subdir, which are Mesop apps and not actually part of
    # the core Mesop framework.
    #
    # "site-packages" is the file path of the Mesop framework when running under pip CLI.
    # If the file is neither of those paths, then we assume it is an app file.
    if (
      "mesop/mesop" not in filename or "mesop/mesop/examples" in filename
    ) and "site-packages" not in filename:
      # Get module from filepath
      splitted_file = filename.split("runfiles/")
      if len(splitted_file) < 2:
        segments = os.path.normpath(splitted_file[0]).split(os.sep)
        segments[-1] = segments[-1][: -len(".py")]
        module = ".".join(segments)
      else:
        segments = os.path.normpath(splitted_file[1]).split(os.sep)
        segments[-1] = segments[-1][: -len(".py")]
        module = ".".join(segments)

      return pb.SourceCodeLocation(
        module=module,
        line=caller_info.lineno,
      )

    current_frame = current_frame.f_back

  return None  # If no suitable frame is found
