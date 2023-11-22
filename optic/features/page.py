from typing import Callable
from optic.runtime import runtime


def page(*, path: str = "/") -> Callable[[Callable[[], None]], Callable[[], None]]:
    def decorator(func: Callable[[], None]) -> Callable[[], None]:
        def wrapper() -> None:
            return func()

        runtime.register_path_fn(path, wrapper)
        return wrapper

    return decorator
