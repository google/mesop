from typing import Callable, Any


def page(path: str) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Registers the page with the path with runtime library.
            return func(*args, **kwargs)

        return wrapper

    return decorator
