from typing import Callable, TypeVar, Generic, Dict, Any
from optic.lib.runtime import runtime
import protos.ui_pb2 as pb

# Define a type variable for the state
S = TypeVar('S')

# Define a type for the action
class Action:
    def __init__(self, type: str, payload: pb.UserAction):
        self.type = type
        self.payload = payload

# Define a type for the reducer function
Reducer = Callable[[S, Action], S]

class Store(Generic[S]):
    def __init__(self, reducer: Reducer[S], initial_state: S):
        self.state = initial_state
        self.reducer = reducer

    def dispatch(self, action: Action):
        self.state = self.reducer(self.state, action)

    def get_state(self) -> S:
        return self.state


def store(reducer: Reducer[S], initial_state: S) -> Store[S]:
    new_store = Store(reducer, initial_state)
    current_action = runtime.session().current_action()
    action = Action(type=current_action.action_type.type, payload=current_action)
    new_store.dispatch(action)
    return new_store
