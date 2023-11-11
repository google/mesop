from typing import Any, Callable, Dict, TypeVar, Generic, cast
import protos.ui_pb2 as pb

# Define a type variable for the state
S = TypeVar("S")

# (State, Payload) -> State
Reducer = Callable[[S, Any], S]


class Store(Generic[S]):
    def __init__(self, initial_state: S):
        self.state = initial_state
        self.reducers: Dict[str, Reducer[S]] = {}

    def dispatch(self, action: pb.UserAction):
        payload = cast(Any, action)
        reducer = self.reducers.get(action.action_type.type)
        if reducer:
            return reducer(self.state, payload)
        else:
            print(
                f"Unknown action type: {action.action_type}; reducers={self.reducers}"
            )
            return self.state

    def get_state(self) -> S:
        return self.state
