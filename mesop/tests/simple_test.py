import types

import mesop as me


def test_hello_world():
  assert isinstance(me, types.ModuleType)


if __name__ == "__main__":
  import pytest

  raise SystemExit(pytest.main([__file__]))
