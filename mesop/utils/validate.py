from functools import wraps
from typing import Any, Callable, TypeVar, cast

from pydantic import ValidationError, validate_arguments

from mesop.exceptions import MesopDeveloperException
from mesop.utils.str_utils import snake_case

newline = "\n"
dash = "\\- "

F = TypeVar("F", bound=Callable[..., Any])


def validate(fn: F) -> F:
  validated_fn = validate_arguments(fn)

  @wraps(fn)
  def wrapper(*args: Any, **kw_args: Any):
    try:
      return validated_fn(*args, **kw_args)
    except ValidationError as e:
      component_name = snake_case(e.model.__name__)
      raise MesopDeveloperException(
        f"""from [{component_name}](https://google.github.io/mesop/components/{component_name}/) component:
{newline.join([dash + error['msg'] for error in e.errors()])}"""
      ) from e

  return cast(F, wrapper)
