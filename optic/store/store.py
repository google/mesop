from typing import Any, TypeVar
import optic.lib.runtime as runtime


def store(state: Any) -> None:
    runtime.runtime.set_initial_state(state)


S = TypeVar("S")


def state(state: S) -> S:
    return runtime.runtime.session().state()
