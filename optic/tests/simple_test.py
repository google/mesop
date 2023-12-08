import types

import optic as op


def test_hello_world():
  assert isinstance(op, types.ModuleType)


if __name__ == "__main__":
  import pytest

  raise SystemExit(pytest.main([__file__]))
