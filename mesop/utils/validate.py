from functools import wraps
from typing import Any, Callable, TypeVar, cast

import pydantic

from mesop.exceptions import MesopDeveloperException
from mesop.utils.str_utils import snake_case

newline = "\n"
dash = "\\- "

F = TypeVar("F", bound=Callable[..., Any])

pydantic_major_version = int(pydantic.VERSION.split(".")[0])


def validate(fn: F) -> F:
  if pydantic_major_version >= 2:
    validated_fn = pydantic.validate_call(fn)
  else:
    # Pyright can't type-check v1 API.
    validated_fn = pydantic.validate_arguments(fn)  # type: ignore

  @wraps(fn)
  def wrapper(*args: Any, **kw_args: Any):
    try:
      return validated_fn(*args, **kw_args)  # type: ignore
    except pydantic.ValidationError as e:
      if pydantic_major_version >= 2:
        print("e", e)
        component_name = snake_case(e.title)
        raise MesopDeveloperException(
          f"""from [{component_name}](https://google.github.io/mesop/components/{component_name}/) component:
  {newline.join([dash + "__"
                 +  " ".join(str(element) for element in error['loc']) + '__: '
                 + error['msg'] for error in e.errors()])}"""
        ) from e
      else:
        # Pyright can't type-check v1 API.
        component_name = snake_case(e.model.__name__)  # type: ignore
        raise MesopDeveloperException(
          f"""from [{component_name}](https://google.github.io/mesop/components/{component_name}/) component:
  {newline.join([dash + error['msg'] for error in e.errors()])}"""
        ) from e

  return cast(F, wrapper)
