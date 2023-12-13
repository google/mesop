import json
from dataclasses import asdict, is_dataclass
from typing import Any, Callable, Generator, TypeVar, cast

import mesop.protos.ui_pb2 as pb
from mesop.dataclass_utils import update_dataclass_from_json

T = TypeVar("T")

Handler = Callable[[Any], Generator[None, None, None] | None]


class Context:
  _states: dict[type[Any], object]

  def __init__(
    self,
    get_handler: Callable[[str], Handler | None],
    states: dict[type[Any], object],
  ) -> None:
    self._get_handler = get_handler
    self._current_node = pb.Component()
    self._states = states

  def current_node(self) -> pb.Component:
    return self._current_node

  def set_current_node(self, node: pb.Component) -> None:
    self._current_node = node

  def reset_current_node(self) -> None:
    self._current_node = pb.Component()

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

  def process_event(self, event: pb.UserEvent) -> Generator[None, None, None]:
    for state, proto_state in zip(self._states.values(), event.states.states):
      update_dataclass_from_json(state, proto_state.data)

    if event.HasField("hot_reload"):
      yield  # empty yield so there's one tick of the render loop
      return  # return early b/c there's no event handler for hot reload

    payload = cast(Any, event)
    handler = self._get_handler(event.handler_id)
    if handler:
      result = handler(payload)
      if result is not None:
        yield from result
      else:
        yield
    else:
      print(f"Unknown handler id: {event.handler_id}")
