import os

import pytest

from mesop.server.config import Config, CreateConfigFromEnv, app_config


@pytest.fixture
def set_env():
  os.environ["MESOP_STATE_SESSION_BACKEND"] = "memory"
  yield
  del os.environ["MESOP_STATE_SESSION_BACKEND"]


def test_set_valid_config():
  config = Config(state_session_backend="memory")
  assert config.state_session_backend == "memory"


@pytest.mark.usefixtures("set_env")
def test_create_config_from_env():
  config = CreateConfigFromEnv()
  assert config.state_session_backend == "memory"


def test_create_config_from_env_defaults():
  config = CreateConfigFromEnv()
  assert config.state_session_backend == "none"


def test_app_config_defaults():
  assert app_config.state_session_backend == "none"


if __name__ == "__main__":
  raise SystemExit(pytest.main([__file__]))
