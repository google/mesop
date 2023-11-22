from dataclasses import asdict, is_dataclass
import json
from typing import Any
import protos.ui_pb2 as pb
from optic.dataclass_utils import update_dataclass_from_json
from optic.store import Store


class Session:
    _store: Store[Any]

    def __init__(self, store: Store[Any]) -> None:
        self._current_node = pb.Component()
        self._store = store

    def current_node(self) -> pb.Component:
        return self._current_node

    def set_current_node(self, node: pb.Component) -> None:
        self._current_node = node

    def state(self) -> Any:
        return self._store.state()

    def serialize_state(self) -> pb.State | None:
        state = self.state()
        if is_dataclass(state):
            json_str = json.dumps(asdict(state))
            return pb.State(data=json_str)
        else:
            raise Exception(f"State must be a dataclass. Instead got {state}")

    def process_event(self, event: pb.UserEvent) -> None:
        update_dataclass_from_json(self.state(), event.state.data)
        self._store.dispatch(event)
