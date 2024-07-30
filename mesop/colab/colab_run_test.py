import threading
from typing import Any, Callable

import pytest

from mesop.colab.colab_run import colab_run
from mesop.runtime import runtime
from mesop.utils import colab_utils


class FakeThread:
  def __init__(self, target: Callable[..., Any]) -> None:
    pass

  def start(self) -> None:
    pass


@pytest.fixture(autouse=True)
def setup(monkeypatch: pytest.MonkeyPatch):
  monkeypatch.setattr(threading, "Thread", FakeThread)
  monkeypatch.setattr(colab_utils, "is_running_in_colab", lambda: True)
  monkeypatch.setattr(colab_utils, "is_running_ipython", lambda: True)


def test_colab_run_prod_mode():
  colab_run(prod_mode=True)
  assert runtime().debug_mode is False


def test_colab_run_debug_mode():
  colab_run(prod_mode=False)
  assert runtime().debug_mode is True


if __name__ == "__main__":
  raise SystemExit(pytest.main([__file__]))
