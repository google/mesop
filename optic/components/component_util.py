from typing import Any, Callable


def get_qualified_fn_name(fn: Callable[..., Any]):
    return f"{fn.__module__}.{fn.__name__}"