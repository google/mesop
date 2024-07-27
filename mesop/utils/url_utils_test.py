import pytest

from mesop.utils.url_utils import (
  _escape_url_for_csp,
  _remove_url_query_param,
  sanitize_url_for_csp,
)


@pytest.mark.parametrize(
  "input_url,expected_output",
  [
    ("https://example.com", "https://example.com"),
    ("https://example.com?param=value", "https://example.com"),
    ("https://example.com/?param=value", "https://example.com/"),
    ("https://example.com?param1=value1&param2=value2", "https://example.com"),
    ("https://example.com/path?param=value", "https://example.com/path"),
    (
      "https://example.com:8080/path?param=value",
      "https://example.com:8080/path",
    ),
    ("http://example.com?param=value#fragment", "http://example.com#fragment"),
    ("ftp://example.com?param=value", "ftp://example.com"),
  ],
)
def test_remove_url_query_param(input_url: str, expected_output: str):
  assert _remove_url_query_param(input_url) == expected_output


@pytest.mark.parametrize(
  "input_url,expected_output",
  [
    ("http://example.com/;param=value", "http://example.com/%3Bparam=value"),
    ("http://example.com/,param=value", "http://example.com/%2Cparam=value"),
    (
      "http://example.com;param=value,param2=value2",
      "http://example.com%3Bparam=value%2Cparam2=value2",
    ),
    ("http://example.com", "http://example.com"),
    ("", ""),
  ],
)
def test_escape_url_for_csp(input_url: str, expected_output: str):
  assert _escape_url_for_csp(input_url) == expected_output


@pytest.mark.parametrize(
  "input_url,expected_output",
  [
    (
      "http://example.com/;param=value,param2=value2",
      "http://example.com/%3Bparam=value%2Cparam2=value2",
    ),
    ("http://example.com", "http://example.com"),
    ("http://example.com/?query=param", "http://example.com/"),
    (
      "http://example.com/;param=value?query=param",
      "http://example.com/%3Bparam=value",
    ),
    (
      "http://example.com/,param=value?query=param",
      "http://example.com/%2Cparam=value",
    ),
    ("", ""),
  ],
)
def test_sanitize_url_for_csp(input_url: str, expected_output: str):
  assert sanitize_url_for_csp(input_url) == expected_output


if __name__ == "__main__":
  raise SystemExit(pytest.main([__file__]))
