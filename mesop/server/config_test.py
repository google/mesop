import os
from pathlib import Path

import pytest

from mesop.server.config import Config, CreateConfigFromEnv, app_config


@pytest.fixture
def clear_mesop_env():
  yield
  for env_name in os.environ:
    if env_name.startswith("MESOP_"):
      del os.environ[env_name]


def test_set_valid_config():
  config = Config(state_session_backend="memory")
  assert config.state_session_backend == "memory"


@pytest.mark.usefixtures("clear_mesop_env")
def test_create_config_from_env():
  os.environ["MESOP_STATE_SESSION_BACKEND"] = "memory"
  config = CreateConfigFromEnv()
  assert config.state_session_backend == "memory"


def test_create_config_from_env_defaults():
  config = CreateConfigFromEnv()
  assert config.state_session_backend == "none"


def test_app_config_defaults():
  assert app_config.state_session_backend == "none"


@pytest.mark.usefixtures("clear_mesop_env")
def test_state_session_backend_file():
  os.environ["MESOP_STATE_SESSION_BACKEND"] = "file"
  os.environ["MESOP_STATE_SESSION_BACKEND_FILE_BASE_DIR"] = (
    "/tmp/mesop-sessions"
  )
  config = CreateConfigFromEnv()
  assert config.state_session_backend == "file"
  assert config.state_session_backend_file_base_dir == Path(
    "/tmp/mesop-sessions"
  )


@pytest.mark.usefixtures("clear_mesop_env")
def test_state_session_backend_firestore():
  os.environ["MESOP_STATE_SESSION_BACKEND"] = "firestore"
  os.environ["MESOP_STATE_SESSION_BACKEND_FIRESTORE_COLLECTION"] = "collection"
  config = CreateConfigFromEnv()
  assert config.state_session_backend == "firestore"
  assert config.state_session_backend_firestore_collection == "collection"


@pytest.mark.usefixtures("clear_mesop_env")
def test_state_session_backend_sql():
  os.environ["MESOP_STATE_SESSION_BACKEND"] = "sql"
  os.environ["MESOP_STATE_SESSION_BACKEND_SQL_CONNECTION_URI"] = (
    "connection://uri"
  )
  os.environ["MESOP_STATE_SESSION_BACKEND_SQL_TABLE"] = "session"
  config = CreateConfigFromEnv()
  assert config.state_session_backend == "sql"
  assert config.state_session_backend_sql_connection_uri == "connection://uri"
  assert config.state_session_backend_sql_table == "session"


if __name__ == "__main__":
  raise SystemExit(pytest.main([__file__]))
