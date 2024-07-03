import logging
import os
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Protocol

import msgpack

from mesop.dataclass_utils import (
  serialize_dataclass,
  update_dataclass_from_json,
)
from mesop.server.config import Config, app_config

States = dict[type[Any], object]


def _current_datetime():
  """Helper to return datetime now so we can mock the time easier."""
  return datetime.now()


class StateSessionBackend(Protocol):
  """Interface for state session backends."""

  def restore(self, token: str, states: States):
    """Gets the saved state from the given token and updates the given state."""
    raise NotImplementedError()

  def save(self, token: str, states: States):
    """Saves state to the backend with the given token."""
    raise NotImplementedError()

  def clear_stale_sessions(self):
    """Deletes unused state data."""
    raise NotImplementedError()


class NullStateSessionBackend(StateSessionBackend):
  """State session backend used when state sessions are disabled."""

  def restore(self, token: str, states: States):
    raise Exception("No state session backend configured.")

  def save(self, token: str, states: States):
    pass

  def clear_stale_sessions(self):
    pass


class MemoryStateSessionBackend(StateSessionBackend):
  """Stores state in memory.

  The main limitation of this backend is that deloyments with multiple processes /
  replicas / instances will cause a lot of cache misses if there is no session affinity.

  This is because memory is local to each Mesop server process.

  In addition, memory should be allocated carefully to the amount of traffic and state
  size that will be expected by the Mesop app.
  """

  # Hardcode for now, but probably make adjustable in the future.
  _SESSION_TTL_MINUTES = 10

  def __init__(self):
    self.cache = {}

  def restore(self, token: str, states: States):
    if token not in self.cache:
      raise Exception("Token not found in state session backend.")
    _, cached_states = self.cache[token]
    for key, cached_state in cached_states.items():
      states[key] = cached_state

    # Delete the cache instance each time since a temporary state may be used.
    del self.cache[token]

  def save(self, token: str, states: States):
    self.cache[token] = (_current_datetime(), states)

  def clear_stale_sessions(self):
    stale_keys = set()

    current_time = _current_datetime()
    for key, (timestamp, _) in self.cache.items():
      if (
        timestamp + timedelta(minutes=self._SESSION_TTL_MINUTES) < current_time
      ):
        stale_keys.add(key)

    for key in stale_keys:
      del self.cache[key]


class FileStateSessionBackend(StateSessionBackend):
  """Stores state on the filesystem.

  This backend allows state to be shared across processes on the same server. If session
  affinity is not available, then the only way to improve performance is to scale
  vertically.

  The main bottleneck is disk read/write performance. If using this backend, you should
  load test against expected traffic and state size to see if this backend meets your
  needs.
  """

  # Hardcode for now, but probably make adjustable in the future.
  _SESSION_TTL_MINUTES = 10
  # Rate in which we will attempt to clear stale sessions. This is done to
  # to reduce concurrent attempts to delete stale sessions.
  #
  # Example: If the rate is set to 0.1, that means the clear state sessions function
  # will run 1 in 10 requests or 10% of the time.
  _SESSION_CLEAR_RATE = 0.1

  def __init__(self, base_dir: Path):
    if base_dir is None:
      raise RuntimeError(
        "Base dir must be set when using `FileStateSessionBackend`"
      )
    self.base_dir = base_dir
    self.prefix = "session"

  def _make_file_path(self, token: str) -> Path:
    return self.base_dir / (self.prefix + token)

  def restore(self, token: str, states: States):
    """Gets the saved state from the given token and updates the given state."""
    file_path = self._make_file_path(token)
    try:
      with open(file_path, "rb") as f:
        states_data = msgpack.unpackb(f.read())
      _deserialize_state(states, states_data)
    except FileNotFoundError as e:
      raise Exception("Token not found in state session backend.") from e
    else:
      try:
        os.remove(file_path)
      except FileNotFoundError as e:
        logging.warning("Failed to delete file after restore - " + str(e))

  def save(self, token: str, states: States):
    """Saves state to the backend with the given token."""
    with open(self._make_file_path(token), "wb") as f:
      f.write(msgpack.packb(_serialize_state(states)))  # type: ignore

  def clear_stale_sessions(self):
    """Deletes unused state data."""
    if random.random() > self._SESSION_CLEAR_RATE:
      return

    for filename in os.listdir(self.base_dir):
      file_path = self.base_dir / filename
      current_time = _current_datetime()
      if os.path.isfile(file_path) and filename.startswith(self.prefix):
        timestamp = datetime.fromtimestamp(os.path.getctime(file_path))
        if (
          timestamp + timedelta(minutes=self._SESSION_TTL_MINUTES)
          < current_time
        ):
          try:
            os.remove(file_path)
          except FileNotFoundError as e:
            logging.warning(
              "Failed to delete file while clearing sessions - " + str(e)
            )


def CreateStateSessionFromConfig(config: Config):
  """Factory function to state session backend."""
  if config.state_session_backend == "memory":
    return MemoryStateSessionBackend()
  elif config.state_session_backend == "file":
    return FileStateSessionBackend(config.state_session_backend_file_base_dir)
  return NullStateSessionBackend()


# The state session is a singleton object.
state_session = CreateStateSessionFromConfig(app_config)


def _serialize_state(states: States) -> list[str]:
  states_data = []
  for state in states.values():
    states_data.append(serialize_dataclass(state))
  return states_data


def _deserialize_state(states: States, states_data: list[str]):
  for state, serialized_state in zip(states.values(), states_data):
    update_dataclass_from_json(state, serialized_state)
