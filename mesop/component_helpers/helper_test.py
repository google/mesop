import pytest

from mesop.component_helpers.helper import check_attribute_keys_is_safe
from mesop.exceptions import MesopDeveloperException


def test_check_attribute_keys_is_safe_raises_exception():
  with pytest.raises(MesopDeveloperException):
    check_attribute_keys_is_safe({"src": None}.keys())
  with pytest.raises(MesopDeveloperException):
    check_attribute_keys_is_safe({"SRC": None}.keys())

  with pytest.raises(MesopDeveloperException):
    check_attribute_keys_is_safe({"srcdoc": None}.keys())

  with pytest.raises(MesopDeveloperException):
    check_attribute_keys_is_safe({"on": None}.keys())
  with pytest.raises(MesopDeveloperException):
    check_attribute_keys_is_safe({"On": None}.keys())
  with pytest.raises(MesopDeveloperException):
    check_attribute_keys_is_safe({"ON": None}.keys())
  with pytest.raises(MesopDeveloperException):
    check_attribute_keys_is_safe({"onClick": None}.keys())


def test_check_attribute_keys_is_safe_passes():
  check_attribute_keys_is_safe({"a": None}.keys())
  check_attribute_keys_is_safe({"decrement": None}.keys())
  check_attribute_keys_is_safe({"click-on": None}.keys())


if __name__ == "__main__":
  raise SystemExit(pytest.main([__file__]))
