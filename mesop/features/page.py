from typing import Callable

from mesop.runtime import runtime


def page(
  *,
  path: str = "/",
  title: str | None = None,
) -> Callable[[Callable[[], None]], Callable[[], None]]:
  def decorator(func: Callable[[], None]) -> Callable[[], None]:
    def wrapper() -> None:
      return func()

    runtime().register_path_fn(path, wrapper)
    runtime().register_path_title(path, title or f"Mesop: {path}")
    return wrapper

  return decorator
