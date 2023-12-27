from typing import Any, Callable, Generator, TypeVar, cast

import mesop.protos.ui_pb2 as pb
from mesop.dataclass_utils import (
  serialize_dataclass,
  update_dataclass_from_json,
)
from mesop.exceptions import MesopDeveloperException, MesopException

T = TypeVar("T")

Handler = Callable[[Any], Generator[None, None, None] | None]


class Context:
  _states: dict[type[Any], object]
  _handlers: dict[str, Handler]
  _commands: list[pb.Command]
  _node_slot: pb.Component | None
  _node_slot_children_count: int | None

  def __init__(
    self,
    get_handler: Callable[[str], Handler | None],
    states: dict[type[Any], object],
  ) -> None:
    self._get_handler = get_handler
    self._current_node = pb.Component()
    self._states = states
    self._trace_mode = False
    self._handlers = {}
    self._commands = []
    self._node_slot = None
    self._node_slot_children_count = None

  def commands(self) -> list[pb.Command]:
    return self._commands

  def navigate(self, url: str) -> None:
    self._commands.append(pb.Command(navigate=pb.NavigateCommand(url=url)))

  def register_event_handler(self, fn_id: str, handler: Handler) -> None:
    if self._trace_mode:
      self._handlers[fn_id] = handler

  def set_trace_mode(self, trace_mode: bool) -> None:
    self._trace_mode = trace_mode

  def current_node(self) -> pb.Component:
    return self._current_node

  def save_current_node_as_slot(self) -> None:
    self._node_slot = self._current_node
    self._node_slot_children_count = len(self._current_node.children)

  def node_slot(self) -> pb.Component | None:
    return self._node_slot

  def node_slot_children_count(self) -> int | None:
    return self._node_slot_children_count

  def set_current_node(self, node: pb.Component) -> None:
    self._current_node = node

  def reset_current_node(self) -> None:
    self._current_node = pb.Component()

  def state(self, state: type[T]) -> T:
    if state not in self._states:
      raise MesopDeveloperException(
        f"""Tried to get the state instance for `{state.__name__}`, but it's not a state class.

Did you forget to decorate your state class `{state.__name__}` with @stateclass?"""
      )
    return cast(T, self._states[state])

  def serialize_state(self) -> pb.States:
    states = pb.States()
    for state in self._states.values():
      states.states.append(pb.State(data=serialize_dataclass(state)))
    return states

  def update_state(self, states: pb.States) -> None:
    for state, proto_state in zip(self._states.values(), states.states):
      update_dataclass_from_json(state, proto_state.data)

  def run_event_handler(
    self, event: pb.UserEvent
  ) -> Generator[None, None, None]:
    if event.HasField("navigation"):
      yield  # empty yield so there's one tick of the render loop
      return  # return early b/c there's no event handler for hot reload

    payload = cast(Any, event)
    handler = self._handlers.get(event.handler_id)
    if handler:
      result = handler(payload)
      if result is not None:
        yield from result
      else:
        yield
    else:
      raise MesopException(
        f"Unknown handler id: {event.handler_id} from event {event}"
      )
