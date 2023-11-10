from dataclasses import asdict, fields, is_dataclass
import json
from typing import Callable, TypeVar, Generic, Any
from optic.lib.runtime import runtime
import protos.ui_pb2 as pb

# Define a type variable for the state
S = TypeVar("S")


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
    current_state = runtime.session().current_state()
    if current_state is not None:
        update_dataclass_from_json(initial_state, current_state.data)

    new_store = Store(reducer, initial_state)

    current_action = runtime.session().current_action()
    action = Action(type=current_action.action_type.type, payload=current_action)
    new_store.dispatch(action)
    new_state = new_store.get_state()
    if is_dataclass(new_state):
        json_str = json.dumps(asdict(new_state))
        runtime.session().set_current_state(pb.State(data=json_str))
    else:
        raise Exception(f"State must be a dataclass. Instead got {new_state}")

    return new_store


def clear_dataclass(instance: Any):
    for field in fields(instance):
        setattr(instance, field.name, field.default)


def update_dataclass_from_json(instance: Any, json_string: str):
    clear_dataclass(instance)  # Clear the instance first
    data = json.loads(json_string)
    for key, value in data.items():
        if hasattr(instance, key):
            setattr(instance, key, value)
