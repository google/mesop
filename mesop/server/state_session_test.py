from dataclasses import dataclass
from datetime import datetime, timedelta

import pytest

from mesop.server.config import Config
from mesop.server.state_session import (
  CreateStateSessionFromConfig,
  MemoryStateSessionBackend,
  NullStateSessionBackend,
  States,
)


@dataclass
class StateA:
  str_value: str = ""


@dataclass
class StateB:
  int_value: int = 0
  bool_value: bool = True


@pytest.mark.parametrize(
  "backend,expected_backend",
  [
    ("none", NullStateSessionBackend),
    ("memory", MemoryStateSessionBackend),
  ],
)
def test_create_state_session_from_config(backend, expected_backend):
  assert isinstance(
    CreateStateSessionFromConfig(Config(state_session_backend=backend)),
    expected_backend,
  )


def test_null_backend_restore_raises_exception():
  backend = NullStateSessionBackend()
  with pytest.raises(Exception, match="No state session backend configured."):
    backend.restore("test", {})


def test_null_backend_save_is_noop():
  backend = NullStateSessionBackend()
  backend.save("test", {})


def test_null_backend_clear_stale_sessions_is_noop():
  backend = NullStateSessionBackend()
  backend.clear_stale_sessions()


def test_memory_backend_restore_token_not_found_returns_exception():
  backend = MemoryStateSessionBackend()
  with pytest.raises(
    Exception, match="Token not found in state session backend."
  ):
    backend.restore("test", {})


def test_memory_backend_save_and_restore_states():
  # GIVEN
  empty_states: States = {
    type(StateA): StateA(),
    type(StateB): StateB(),
  }
  saved_states: States = {
    type(StateA): StateA(str_value="ABC"),
    type(StateB): StateB(int_value=20, bool_value=False),
  }
  backend = MemoryStateSessionBackend()
  backend.save("test", saved_states)

  # WHEN
  backend.restore("test", empty_states)

  # THEN
  assert empty_states == saved_states


def test_memory_backend_token_is_cleared_after_restore():
  # GIVEN
  empty_states: States = {
    type(StateA): StateA(),
    type(StateB): StateB(),
  }
  saved_states: States = {
    type(StateA): StateA(str_value="ABC"),
    type(StateB): StateB(int_value=20, bool_value=False),
  }
  backend = MemoryStateSessionBackend()
  backend.save("test", saved_states)
  backend.restore("test", empty_states)

  # WHEN / THEN
  with pytest.raises(
    Exception, match="Token not found in state session backend."
  ):
    backend.restore("test", empty_states)


def test_memory_backend_clear_stale_sessions():
  # GIVEN
  empty_states: States = {
    type(StateA): StateA(str_value="ABC"),
  }
  backend = MemoryStateSessionBackend()
  backend.cache = {
    "key1": (datetime.now() - timedelta(minutes=11), {type(StateA): StateA()}),
    "key2": (datetime.now(), {type(StateA): StateA()}),
    "key3": (datetime.now() - timedelta(minutes=12), {type(StateA): StateA()}),
  }

  # WHEN
  backend.clear_stale_sessions()

  # THEN
  with pytest.raises(
    Exception, match="Token not found in state session backend."
  ):
    backend.restore("key1", empty_states)
  with pytest.raises(
    Exception, match="Token not found in state session backend."
  ):
    backend.restore("key3", empty_states)
  backend.restore("key2", empty_states)
  assert empty_states == {type(StateA): StateA()}


if __name__ == "__main__":
  raise SystemExit(pytest.main([__file__]))
