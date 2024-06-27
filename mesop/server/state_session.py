from datetime import datetime, timedelta
from typing import Any, Protocol

from mesop.server.config import Config, app_config

States = dict[type[Any], object]


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
    self.cache[token] = (datetime.now(), states)

  def clear_stale_sessions(self):
    stale_keys = set()

    current_time = datetime.now()
    for key, (timestamp, _) in self.cache.items():
      if (
        timestamp + timedelta(minutes=self._SESSION_TTL_MINUTES) < current_time
      ):
        stale_keys.add(key)

    for key in stale_keys:
      del self.cache[key]


def CreateStateSessionFromConfig(config: Config):
  """Factory function to state session backend."""
  if config.state_session_backend == "memory":
    return MemoryStateSessionBackend()
  return NullStateSessionBackend()


# The state session is a singleton object.
state_session = CreateStateSessionFromConfig(app_config)
