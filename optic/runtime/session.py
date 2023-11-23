from dataclasses import asdict, is_dataclass
import json
from typing import Any, TypeVar, cast
import protos.ui_pb2 as pb
from optic.dataclass_utils import update_dataclass_from_json
from optic.store import Store

T = TypeVar("T")


class Session:
    _store: Store[Any]
    _states: dict[type[Any], object]

    def __init__(self, store: Store[Any], states: dict[type[Any], object]) -> None:
        self._current_node = pb.Component()
        self._store = store
        self._states = states

    def current_node(self) -> pb.Component:
        return self._current_node

    def set_current_node(self, node: pb.Component) -> None:
        self._current_node = node

    def state(self, state: type[T]) -> T:
        return cast(T, self._states[state])

    def serialize_state(self) -> pb.States:
        states = pb.States()
        for state in self._states.values():
            if is_dataclass(state):
                json_str = json.dumps(asdict(state))
                states.states.append(pb.State(data=json_str))
            else:
                raise Exception(f"State must be a dataclass. Instead got {state}")
        return states

    def process_event(self, event: pb.UserEvent) -> None:
        for state, proto_state in zip(self._states.values(), event.states.states):
            update_dataclass_from_json(state, proto_state.data)
        self._store.dispatch(event)
