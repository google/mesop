from typing import Callable

from mesop.runtime import PageConfig, runtime
from mesop.security.security_policy import SecurityPolicy


def page(
  *,
  path: str = "/",
  title: str | None = None,
  security_policy: SecurityPolicy | None = None,
) -> Callable[[Callable[[], None]], Callable[[], None]]:
  def decorator(func: Callable[[], None]) -> Callable[[], None]:
    def wrapper() -> None:
      return func()

    runtime().register_page(
      path=path,
      page_config=PageConfig(
        page_fn=wrapper,
        title=title or f"Mesop: {path}",
        security_policy=security_policy
        if security_policy
        else SecurityPolicy(),
      ),
    )
    return wrapper

  return decorator
