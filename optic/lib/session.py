from dataclasses import asdict, is_dataclass
import json
from typing import Any
import protos.ui_pb2 as pb
from ..state.serialization import update_dataclass_from_json
from ..state.state import Store


class Session:
    _current_state: pb.State | None
    _store: Store[Any]

    def __init__(self) -> None:
        self._current_node = pb.Component()
        self._current_action = pb.UserEvent()
        self._current_state = None

    def current_node(self) -> pb.Component:
        return self._current_node

    def set_current_node(self, node: pb.Component) -> None:
        self._current_node = node

    def current_action(self) -> pb.UserEvent:
        return self._current_action

    def current_state(self) -> pb.State | None:
        return self._current_state

    def set_current_state(self, state: pb.State) -> None:
        self._current_state = state

    def set_current_action(self, action: pb.UserEvent) -> None:
        self._current_action = action

    def execute_current_action(self) -> None:
        current_action = self.current_action()
        self._store.dispatch(current_action)
        new_state = self._store.get_state()
        if is_dataclass(new_state):
            json_str = json.dumps(asdict(new_state))
            self.set_current_state(pb.State(data=json_str))
        else:
            raise Exception(f"State must be a dataclass. Instead got {new_state}")

    def create_store(self, initial_state: Any) -> Store[Any]:
        current_state = self.current_state()
        if current_state is not None and len(current_state.data) > 0:
            update_dataclass_from_json(initial_state, current_state.data)

        new_store = Store(initial_state)

        self._store = new_store
        print("*** new_store", new_store)
        return new_store

    def get_store(self) -> Store[Any]:
        return self._store
