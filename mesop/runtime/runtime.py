from dataclasses import dataclass
from typing import Any, Callable, Generator, Type, TypeVar, cast

from flask import g

import mesop.protos.ui_pb2 as pb
from mesop.events import MesopEvent
from mesop.exceptions import MesopUserException
from mesop.key import Key
from mesop.utils.backoff import exponential_backoff

from .context import Context

Handler = Callable[[Any], None | Generator[None, None, None]]
newline = "\n"


@dataclass
class EmptyState:
  pass


E = TypeVar("E", bound=MesopEvent)
T = TypeVar("T")


class Runtime:
  _path_fns: dict[str, Callable[[], None]]
  _path_title: dict[str, str]
  _handlers: dict[str, Handler]
  _state_classes: list[type[Any]]
  _loading_errors: list[pb.ServerError]
  component_fns: set[Callable[..., Any]]
  debug_mode: bool = False
  is_hot_reload_in_progress: bool = False

  def __init__(self):
    self.component_fns = set()
    self._path_fns = {}
    self._path_title = {}
    self._handlers = {}
    self.event_mappers: dict[Type[Any], Callable[[pb.UserEvent, Key], Any]] = {}
    self._state_classes = []
    self._loading_errors = []

  def context(self) -> Context:
    if "context" not in g:
      g.context = self.create_context()
    return g.context

  def create_context(self) -> Context:
    if len(self._state_classes) == 0:
      states = {EmptyState: EmptyState()}
    else:
      states = {}
      # Create new instances so that we don't accidentally share state across contexts.
      for state_class in self._state_classes:
        states[state_class] = state_class()

    return Context(
      get_handler=self.get_handler, states=cast(dict[Any, Any], states)
    )

  def wait_for_hot_reload(self):
    # If hot reload is in-progress, the path may not be registered yet because the client reload
    # happened before the server module re-execution completed.
    if self.is_hot_reload_in_progress:
      exponential_backoff(
        lambda: not self.is_hot_reload_in_progress, initial_delay=0.100
      )

  def run_path(self, path: str, trace_mode: bool = False) -> None:
    self.context().set_trace_mode(trace_mode)

    if path not in self._path_fns:
      paths = list(self._path_fns.keys())
      if not paths:
        raise MesopUserException(
          "No page has been registered. Read the [page docs](https://google.github.io/mesop/guides/pages/) to configure a page."
        )
      paths.sort()
      raise MesopUserException(
        f"""Accessed path: {path} not registered

Try one of the following paths:
{newline.join([f"[{p}]({p})" for p in paths])}
                                     """
      )
    self._path_fns[path]()

  def register_path_fn(self, path: str, fn: Callable[[], None]) -> None:
    self._path_fns[path] = fn

  def register_path_title(self, path: str, title: str) -> None:
    self._path_title[path] = title

  def get_path_title(self, path: str) -> str:
    return self._path_title[path]

  def register_handler(self, handler_id: str, handler: Handler) -> None:
    self._handlers[handler_id] = handler

  def get_handler(self, handler_id: str) -> Handler | None:
    return self._handlers[handler_id]

  def register_state_class(self, state_class: Any) -> None:
    self._state_classes.append(state_class)

  def add_loading_error(self, error: pb.ServerError) -> None:
    """Only put non-context specific errors, because these errors can be potentially shown across contexts."""
    self._loading_errors.append(error)

  def has_loading_errors(self) -> bool:
    return len(self._loading_errors) > 0

  def get_loading_errors(self) -> list[pb.ServerError]:
    return self._loading_errors

  def register_native_component_fn(self, component_fn: Callable[..., Any]):
    self.component_fns.add(component_fn)

  def get_component_fns(self) -> set[Callable[..., Any]]:
    return self.component_fns

  def register_event_mapper(
    self, event: Type[E], map_fn: Callable[[pb.UserEvent, Key], E]
  ):
    self.event_mappers[event] = map_fn

  def get_event_mapper(
    self, event: Type[E]
  ) -> Callable[[pb.UserEvent, Key], E]:
    return self.event_mappers[event]


_runtime = Runtime()


def runtime():
  return _runtime


def reset_runtime():
  global _runtime
  old_runtime = _runtime
  _runtime = Runtime()
  _runtime.is_hot_reload_in_progress = True
  _runtime.debug_mode = old_runtime.debug_mode
  _runtime.component_fns = old_runtime.component_fns
  _runtime.event_mappers = old_runtime.event_mappers


def enable_debug_mode():
  _runtime.debug_mode = True


def hot_reload_finished():
  _runtime.is_hot_reload_in_progress = False
