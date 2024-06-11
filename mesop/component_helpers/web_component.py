from functools import wraps
from typing import Any, Callable, TypeVar, cast

from mesop.runtime import runtime

C = TypeVar("C", bound=Callable[..., Any])


def web_component(js_path: str):
  def component_wrapper(fn: C) -> C:
    @wraps(fn)
    def wrapper(*args: Any, **kw_args: Any):
      fn(*args, **kw_args)

    return cast(C, wrapper)

  with open(js_path) as js_file:
    js_content = js_file.read()
  runtime().register_js_script(js_content)
  return component_wrapper
