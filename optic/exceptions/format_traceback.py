import traceback
import sys
import linecache

import protos.ui_pb2 as pb


def format_traceback(lines_before: int = 2, lines_after: int = 4) -> pb.Traceback:
    # Initialize an empty string to accumulate traceback information
    res = pb.Traceback(frames=[])

    # Capture the current exception's traceback
    _, _, exc_traceback = sys.exc_info()

    # Iterate through the stack trace
    for frame, lineno in traceback.walk_tb(exc_traceback):
        filename = frame.f_code.co_filename
        filename_segments = filename.split(".runfiles")
        code_name = frame.f_code.co_name
        stack_frame = pb.StackFrame(
            filename=filename_segments[len(filename_segments) - 1],
            code_name=code_name,
            line_number=lineno,
            lines=[],
            is_app_code=code_name == "<module>",
        )

        start_line = max(1, lineno - lines_before)
        end_line = lineno + lines_after
        for i in range(start_line, end_line + 1):
            code = linecache.getline(filename, i).strip()
            if len(code) > 0:
                stack_frame.lines.append(
                    pb.ContextLine(code=code, is_caller=i == lineno)
                )
        res.frames.append(stack_frame)

    return res
