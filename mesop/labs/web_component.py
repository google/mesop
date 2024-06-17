import inspect
import os
from functools import wraps
from typing import Any, Callable, TypeVar, cast

from mesop.runtime import runtime
from mesop.utils.validate import validate

C = TypeVar("C", bound=Callable[..., Any])


def web_component(*, path: str, skip_validation: bool = False):
  """A decorator for defining a web component.

  This decorator is used to define a web component. It takes a path to the
  JavaScript file of the web component and an optional parameter to skip
  validation. It then registers the JavaScript file in the runtime.

  Args:
    path: The path to the JavaScript file of the web component.
    skip_validation: If set to True, skips validation. Defaults to False.
  """
  current_frame = inspect.currentframe()
  assert current_frame
  previous_frame = current_frame.f_back
  assert previous_frame
  caller_module_file = inspect.getfile(previous_frame)
  caller_module_dir = format_filename(
    os.path.dirname(os.path.abspath(caller_module_file))
  )
  full_path = os.path.normpath(os.path.join(caller_module_dir, path))
  if not full_path.startswith("/"):
    full_path = "/" + full_path

  runtime().register_js_module(full_path)

  def component_wrapper(fn: C) -> C:
    validated_fn = fn if skip_validation else validate(fn)

    @wraps(fn)
    def wrapper(*args: Any, **kw_args: Any):
      return validated_fn(*args, **kw_args)

    return cast(C, wrapper)

  return component_wrapper


def format_filename(filename: str) -> str:
  if ".runfiles" in filename:
    # Handle Bazel case
    return filename.split(".runfiles", 1)[1]
  else:
    # Handle pip CLI case
    return os.path.relpath(filename, os.getcwd())
