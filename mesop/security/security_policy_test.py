import pytest

from mesop.exceptions import MesopDeveloperException
from mesop.security.security_policy import SecurityPolicy


def test_default_security_policy_is_valid():
  policy = SecurityPolicy()
  assert policy.dangerously_disable_trusted_types is False


def test_disable_trusted_types_and_configuring_trusted_types_raises_exception():
  with pytest.raises(MesopDeveloperException) as e:
    SecurityPolicy(
      allowed_trusted_types=["ttpolicy1", "ttpolicy2"],
      dangerously_disable_trusted_types=True,
    )
    assert (
      "Cannot disable trusted types and configure allow trusted types on SecurityPolicy at the same time"
      in str(e.value)
    )


def test_configuring_trusted_types_without_disabling_trusted_types():
  try:
    SecurityPolicy(
      allowed_trusted_types=["ttpolicy1", "ttpolicy2"],
      dangerously_disable_trusted_types=False,
    )
  except MesopDeveloperException:
    pytest.fail("MesopDeveloperException was raised unexpectedly!")


def test_disabling_trusted_types_without_configuring_trusted_types():
  try:
    SecurityPolicy(
      allowed_trusted_types=[],
      dangerously_disable_trusted_types=True,
    )
  except MesopDeveloperException:
    pytest.fail("MesopDeveloperException was raised unexpectedly!")


if __name__ == "__main__":
  raise SystemExit(pytest.main([__file__]))
