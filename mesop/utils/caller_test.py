import pytest

import mesop.protos.ui_pb2 as pb
from mesop.utils.caller import get_caller_source_code_location


def wrap1():
  return get_caller_source_code_location(levels=2)


def wrap2():
  return wrap1()


def test_source_code_location():
  assert wrap2() == pb.SourceCodeLocation(
    module="mesop.mesop.utils.caller_test", line=12
  )


if __name__ == "__main__":
  raise SystemExit(pytest.main([__file__]))
