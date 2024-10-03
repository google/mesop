import asyncio
import copy
import types
import urllib.parse as urlparse
from typing import Any, Callable, Generator, Sequence, TypeVar, cast

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
from mesop.server.state_session import state_session

T = TypeVar("T")

Handler = Callable[[Any], Generator[None, None, None] | None]


class Context:
  def __init__(
    self,
    get_handler: Callable[[str], Handler | None],
    states: dict[type[Any], object],
  ) -> None:
    self._get_handler = get_handler
    self._current_node = pb.Component()
    self._previous_node: pb.Component | None = None
    self._states: dict[type[Any], object] = states
    # Previous states is used for performing state diffs.
    self._previous_states: dict[type[Any], object] = copy.deepcopy(states)
    self._trace_mode = False
    self._handlers: dict[str, Handler] = {}
    self._commands: list[pb.Command] = []
    self._node_slot: pb.Component | None = None
    self._node_slot_children_count: int | None = None
    self._viewport_size: pb.ViewportSize | None = None
    self._theme_settings: pb.ThemeSettings | None = None
    self._js_modules: set[str] = set()
    self._query_params: dict[str, list[str]] = {}

  def register_js_module(self, js_module_path: str) -> None:
    self._js_modules.add(js_module_path)

  def js_modules(self) -> set[str]:
    return self._js_modules

  def clear_js_modules(self):
    self._js_modules = set()

  def query_params(self) -> dict[str, list[str]]:
    return self._query_params

  def initialize_query_params(self, query_params: Sequence[pb.QueryParam]):
    for query_param in query_params:
      self._query_params[query_param.key] = list(query_param.values)

  def set_query_param(self, key: str, value: str | Sequence[str] | None):
    if value is None:
      del self._query_params[key]
    else:
      self._query_params[key] = (
        [value] if isinstance(value, str) else list(value)
      )
    self._commands.append(
      pb.Command(
        update_query_param=pb.UpdateQueryParam(
          query_param=pb.QueryParam(
            key=key, values=[value] if isinstance(value, str) else value
          )
        )
      )
    )

  def commands(self) -> list[pb.Command]:
    return self._commands

  def clear_commands(self) -> None:
    self._commands = []

  def navigate(
    self, url: str, query_params: dict[str, str | Sequence[str]] | None = None
  ) -> None:
    query_param_protos = None
    if query_params is not None:
      query_param_protos = [
        pb.QueryParam(
          key=key, values=[value] if isinstance(value, str) else value
        )
        for key, value in query_params.items()
      ]
    # Construct the full URL with query parameters
    full_url = url
    if query_params:
      query_string = "&".join(
        f"{urlparse.quote(key)}={urlparse.quote(value)}"
        if isinstance(value, str)
        else "&".join(
          f"{urlparse.quote(key)}={urlparse.quote(v)}" for v in value
        )
        for key, value in query_params.items()
      )
      full_url += f"?{query_string}"

    self._commands.append(
      pb.Command(
        navigate=pb.NavigateCommand(
          url=full_url, query_params=query_param_protos
        )
      )
    )

  def scroll_into_view(self, key: str) -> None:
    self._commands.append(
      pb.Command(scroll_into_view=pb.ScrollIntoViewCommand(key=key))
    )

  def focus_component(self, key: str) -> None:
    self._commands.append(
      pb.Command(focus_component=pb.FocusComponentCommand(key=key))
    )

  def set_page_title(self, title: str) -> None:
    self._commands.append(
      pb.Command(set_page_title=pb.SetPageTitle(title=title))
    )

  def set_theme_density(self, density: int) -> None:
    self._commands.append(
      pb.Command(set_theme_density=pb.SetThemeDensity(density=density))
    )

  def set_theme_mode(self, theme_mode: pb.ThemeMode.ValueType) -> None:
    self._commands.append(
      pb.Command(set_theme_mode=pb.SetThemeMode(theme_mode=theme_mode))
    )

  def set_theme_settings(self, settings: pb.ThemeSettings) -> None:
    self._theme_settings = settings

  def using_dark_theme(self) -> bool:
    last_theme_mode_command = None
    for command in reversed(self._commands):
      if command.HasField("set_theme_mode"):
        last_theme_mode_command = command
        break
    assert self._theme_settings
    if last_theme_mode_command is None:
      theme_mode = self._theme_settings.theme_mode
    else:
      theme_mode = last_theme_mode_command.set_theme_mode.theme_mode

    if theme_mode == pb.ThemeMode.THEME_MODE_LIGHT:
      return False
    if theme_mode == pb.ThemeMode.THEME_MODE_DARK:
      return True
    if theme_mode == pb.THEME_MODE_SYSTEM:
      return self._theme_settings.prefers_dark_theme
    raise MesopException("Unhandled theme mode", theme_mode)

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

    This is used for performing component tree diffs.
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

  def restore_state_from_session(self, state_token: str):
    """Updates the current state with the state cached in the state session.

    If the `state_token` is not found in the cache, an exception will be raised.
    """
    state_session.restore(state_token, self._states)
    self._previous_states = copy.deepcopy(self._states)

  def save_state_to_session(self, state_token: str):
    """Caches the current state into the state session."""
    state_session.save(state_token, self._states)

  def clear_stale_state_sessions(self):
    """Deletes old cached state since it will not be used anymore."""
    state_session.clear_stale_sessions()

  def update_state(self, states: pb.States) -> None:
    for state, previous_state, proto_state in zip(
      self._states.values(), self._previous_states.values(), states.states
    ):
      update_dataclass_from_json(state, proto_state.data)
      update_dataclass_from_json(previous_state, proto_state.data)

  def run_event_handler(
    self, event: pb.UserEvent
  ) -> Generator[None, None, None]:
    if (
      event.HasField("navigation")
      or event.HasField("resize")
      or event.HasField("change_prefers_color_scheme")
    ):
      yield  # empty yield so there's one tick of the render loop
      return  # return early b/c there's no event handler for these events.

    payload = cast(Any, event)
    handler = self._handlers.get(event.handler_id)
    if handler:
      result = handler(payload)
      if result is not None:
        if isinstance(result, types.AsyncGeneratorType):
          yield from _run_async_generator(result)
        elif isinstance(result, types.CoroutineType):
          yield _run_coroutine(result)
        else:
          yield from result
      else:
        yield
    else:
      raise MesopException(
        f"Unknown handler id: {event.handler_id} from event {event}"
      )


def _run_async_generator(agen: types.AsyncGeneratorType[None, None]):
  loop = _get_or_create_event_loop()
  try:
    while True:
      yield loop.run_until_complete(agen.__anext__())
  except StopAsyncIteration:
    pass


def _run_coroutine(coroutine: types.CoroutineType):
  loop = _get_or_create_event_loop()
  return loop.run_until_complete(coroutine)


def _get_or_create_event_loop():
  try:
    return asyncio.get_running_loop()
  except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop
