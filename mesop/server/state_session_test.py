from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

import pytest

from mesop.server.config import Config
from mesop.server.state_session import (
  CreateStateSessionFromConfig,
  FileStateSessionBackend,
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


@pytest.fixture
def state_session_backend_factory(tmp_path):
  """Fixture to provide state session backends for parameterized tests."""
  return {
    "memory": MemoryStateSessionBackend(),
    "file": FileStateSessionBackend(tmp_path),
  }


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


def test_create_state_session_file():
  assert isinstance(
    CreateStateSessionFromConfig(
      Config(
        state_session_backend="file",
        state_session_backend_file_base_dir=Path("/tmp"),
      )
    ),
    FileStateSessionBackend,
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


@pytest.mark.parametrize("backend_key", ["memory", "file"])
def test_backend_restore_token_not_found_returns_exception(
  backend_key, state_session_backend_factory
):
  backend = state_session_backend_factory[backend_key]
  with pytest.raises(
    Exception, match="Token not found in state session backend."
  ):
    backend.restore("test", {})


@pytest.mark.parametrize("backend_key", ["memory", "file"])
def test_backend_save_and_restore_states(
  backend_key, state_session_backend_factory
):
  # GIVEN
  backend = state_session_backend_factory[backend_key]
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


@pytest.mark.parametrize("backend_key", ["memory", "file"])
def test_backend_token_is_cleared_after_restore(
  backend_key, state_session_backend_factory
):
  backend = state_session_backend_factory[backend_key]
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


def test_file_backend_clear_stale_sessions_not_stale(tmp_path):
  # GIVEN
  backend = FileStateSessionBackend(tmp_path)
  # Modify the clear rate so that sessions are always cleared.
  backend._SESSION_CLEAR_RATE = 1.0
  empty_states: States = {
    type(StateA): StateA(str_value="ABC"),
  }
  backend.save("key1", {type(StateA): StateA()})

  # WHEN
  with patch(
    "mesop.server.state_session._current_datetime",
  ) as _mock_current_datetime:
    _mock_current_datetime.return_value = datetime.now() - timedelta(minutes=15)
    backend.clear_stale_sessions()

    # THEN
    backend.restore("key1", empty_states)
    assert empty_states == {type(StateA): StateA()}


def test_file_backend_clear_stale_sessions(tmp_path):
  # GIVEN
  backend = FileStateSessionBackend(tmp_path)
  # Modify the clear rate so that sessions are always cleared.
  backend._SESSION_CLEAR_RATE = 1.0
  empty_states: States = {
    type(StateA): StateA(str_value="ABC"),
  }
  backend.save("key1", {type(StateA): StateA()})
  backend.save("key2", {type(StateA): StateA()})

  # WHEN
  with patch(
    "mesop.server.state_session._current_datetime",
  ) as _mock_current_datetime:
    _mock_current_datetime.return_value = datetime.now() + timedelta(minutes=15)
    backend.clear_stale_sessions()

    # THEN
    with pytest.raises(
      Exception, match="Token not found in state session backend."
    ):
      backend.restore("key1", empty_states)
    with pytest.raises(
      Exception, match="Token not found in state session backend."
    ):
      backend.restore("key2", empty_states)


def test_file_backend_clear_stale_sessions_skipped(tmp_path):
  # GIVEN
  backend = FileStateSessionBackend(tmp_path)
  # Modify the clear rate so that sessions are never cleared
  backend._SESSION_CLEAR_RATE = -1.0
  empty_states: States = {
    type(StateA): StateA(str_value="ABC"),
  }
  backend.save("key1", {type(StateA): StateA()})

  # WHEN
  with patch(
    "mesop.server.state_session._current_datetime",
  ) as _mock_current_datetime:
    _mock_current_datetime.return_value = datetime.now() + timedelta(minutes=15)
    backend.clear_stale_sessions()

    # THEN
    backend.restore("key1", empty_states)
    assert empty_states == {type(StateA): StateA()}


if __name__ == "__main__":
  raise SystemExit(pytest.main([__file__]))
