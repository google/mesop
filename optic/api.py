from typing import Any, TypeVar
from optic.runtime import runtime

S = TypeVar("S")


def store(state: Any) -> None:
    runtime.set_initial_state(state)


def state(state: S) -> S:
    return runtime.session().state()
