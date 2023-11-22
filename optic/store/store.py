from typing import Any, TypeVar
from optic.runtime import runtime


def store(state: Any) -> None:
    runtime.set_initial_state(state)


S = TypeVar("S")


def state(state: S) -> S:
    return runtime.session().state()
