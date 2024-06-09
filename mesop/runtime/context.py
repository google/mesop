import copy
from typing import Any, Callable, Generator, TypeVar, cast

from absl import flags

import mesop.protos.ui_pb2 as pb
from mesop.dataclass_utils import (
  diff_state,
  serialize_dataclass,
  update_dataclass_from_json,
)
from mesop.exceptions import (
  MesopDeveloperException,
  MesopException,
)

FLAGS = flags.FLAGS

flags.DEFINE_bool(
  "enable_component_tree_diffs",
  True,
  "set to true to return component tree diffs on user event responses (rather than the full tree).",
)


T = TypeVar("T")

Handler = Callable[[Any], Generator[None, None, None] | None]


class Context:
  _states: dict[type[Any], object]
  # Previous states is used for performing state diffs.
  _previous_states: dict[type[Any], object]
  _handlers: dict[str, Handler]
  _commands: list[pb.Command]
  _node_slot: pb.Component | None
  _node_slot_children_count: int | None
  _viewport_size: pb.ViewportSize | None = None

  def __init__(
    self,
    get_handler: Callable[[str], Handler | None],
    states: dict[type[Any], object],
  ) -> None:
    self._get_handler = get_handler
    self._current_node = pb.Component()
    self._previous_node: pb.Component | None = None
    self._states = states
    self._previous_states = copy.deepcopy(states)
    self._trace_mode = False
    self._handlers = {}
    self._commands = []
    self._node_slot = None
    self._node_slot_children_count = None

  def commands(self) -> list[pb.Command]:
    return self._commands

  def clear_commands(self) -> None:
    self._commands = []

  def navigate(self, url: str) -> None:
    self._commands.append(pb.Command(navigate=pb.NavigateCommand(url=url)))

  def scroll_into_view(self, key: str) -> None:
    self._commands.append(
      pb.Command(scroll_into_view=pb.ScrollIntoViewCommand(key=key))
    )

  def set_viewport_size(self, size: pb.ViewportSize):
    self._viewport_size = size

  def viewport_size(self) -> pb.ViewportSize:
    if self._viewport_size is None:
      raise MesopDeveloperException(
        "Tried to retrieve viewport size before it was set."
      )
    return self._viewport_size

  def register_event_handler(self, fn_id: str, handler: Handler) -> None:
    if self._trace_mode:
      self._handlers[fn_id] = handler

  def set_trace_mode(self, trace_mode: bool) -> None:
    self._trace_mode = trace_mode

  def current_node(self) -> pb.Component:
    return self._current_node

  def previous_node(self) -> pb.Component | None:
    """Used to track the last/previous state of the component tree before the UI updated.

    This is used for performing component tree diffs when the
    `enable_component_tree_diffs` flag is enabled. When previous node is `None`, that
    implies that no component tree diff is to be performed.
    """
    return self._previous_node

  def save_current_node_as_slot(self) -> None:
    self._node_slot = self._current_node
    self._node_slot_children_count = len(self._current_node.children)

  def node_slot(self) -> pb.Component | None:
    return self._node_slot

  def node_slot_children_count(self) -> int | None:
    return self._node_slot_children_count

  def set_current_node(self, node: pb.Component) -> None:
    self._current_node = node

  def set_previous_node_from_current_node(self) -> None:
    # Gate this feature with a flag since this is a new feature and may have some
    # unexpected issues. In addition, some users may have a case where sending the full
    # component tree back on each response is more performant than sending back the
    # diff.
    if FLAGS.enable_component_tree_diffs:
      self._previous_node = self._current_node

  def reset_current_node(self) -> None:
    self._current_node = pb.Component()

  def reset_previous_node(self) -> None:
    self._previous_node = None

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

  def diff_state(self) -> pb.States:
    states = pb.States()
    for state, previous_state in zip(
      self._states.values(), self._previous_states.values()
    ):
      states.states.append(pb.State(data=diff_state(previous_state, state)))
    return states

  def update_state(self, states: pb.States) -> None:
    for state, previous_state, proto_state in zip(
      self._states.values(), self._previous_states.values(), states.states
    ):
      update_dataclass_from_json(state, proto_state.data)
      update_dataclass_from_json(previous_state, proto_state.data)

  def run_event_handler(
    self, event: pb.UserEvent
  ) -> Generator[None, None, None]:
    if event.HasField("navigation") or event.HasField("resize"):
      yield  # empty yield so there's one tick of the render loop
      return  # return early b/c there's no event handler for these events.

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
