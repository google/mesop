from typing import TypeVar
import optic.lib.runtime as runtime
import optic.state as state

S = TypeVar("S")


def store(state: S) -> state.state.Store[S]:
    return runtime.runtime.session().create_store(state)
