import inspect
import os
from functools import wraps
from typing import Any, Callable, TypeVar, cast

from mesop.runtime import runtime

C = TypeVar("C", bound=Callable[..., Any])


def web_component(path: str):
  current_frame = inspect.currentframe()
  assert current_frame
  previous_frame = current_frame.f_back
  assert previous_frame
  caller_module_file = inspect.getfile(previous_frame)
  caller_module_dir = format_filename(
    os.path.dirname(os.path.abspath(caller_module_file))
  )
  full_path = os.path.normpath(os.path.join(caller_module_dir, path))

  # with open(full_path) as js_file:
  #   js_content = js_file.read()
  runtime().register_js_script(full_path)

  def component_wrapper(fn: C) -> C:
    @wraps(fn)
    def wrapper(*args: Any, **kw_args: Any):
      fn(*args, **kw_args)

    return cast(C, wrapper)

  return component_wrapper


def format_filename(filename: str) -> str:
  if ".runfiles" in filename:
    filename = filename.split(".runfiles", 1)[1]
  return filename


# @dataclass(kw_only=True)
# class EventOutput:
#   json: dict[str, Any]
#   key: str


# def register_event_mapper(event: type[_T], map_fn: Callable[[EventOutput], _T]):
#   runtime().register_event_mapper(
#     event=event,
#     map_fn=lambda event, key: map_fn(
#       EventOutput(
#         json=json.loads(event.string_value),
#         key=key.key,
#       )
#     ),
#   )
