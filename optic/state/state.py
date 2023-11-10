from typing import Callable, TypeVar, Generic, Dict, Any

# Define a type variable for the state
S = TypeVar('S')

# Define a type for the action
class Action(Generic[S]):
    def __init__(self, type: str, payload: S):
        self.type = type
        self.payload = payload

# Define a type for the reducer function
Reducer = Callable[[S, Action[S]], S]

class Store(Generic[S]):
    def __init__(self, reducer: Reducer[S], initial_state: S):
        self.state = initial_state
        self.reducer = reducer

    def dispatch(self, action: Action[S]):
        self.state = self.reducer(self.state, action)

    def get_state(self) -> S:
        return self.state


def store(reducer: Reducer[S], initial_state: S) -> Store[S]:
    return Store(reducer, initial_state)
