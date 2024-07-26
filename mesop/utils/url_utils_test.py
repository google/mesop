import pytest

import mesop.protos.ui_pb2 as pb
from mesop.utils.url_utils import (
  _escape_url_for_csp,
  get_url_query_params,
  remove_url_query_param,
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
  assert remove_url_query_param(input_url) == expected_output


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


@pytest.mark.parametrize(
  "input_url,expected_output",
  [
    ("http://example.com", []),
    ("http://example.com?", []),
    (
      "http://example.com?key=value",
      [pb.QueryParam(key="key", values=["value"])],
    ),
    (
      "http://example.com?key1=value1&key2=value2",
      [
        pb.QueryParam(key="key1", values=["value1"]),
        pb.QueryParam(key="key2", values=["value2"]),
      ],
    ),
    (
      "http://example.com?key=value1&key=value2",
      [pb.QueryParam(key="key", values=["value1", "value2"])],
    ),
    ("http://example.com?key=", [pb.QueryParam(key="key", values=[""])]),
    (
      "http://example.com?key1=value1&key2=",
      [
        pb.QueryParam(key="key1", values=["value1"]),
        pb.QueryParam(key="key2", values=[""]),
      ],
    ),
    (
      "http://example.com?key=value#fragment",
      [pb.QueryParam(key="key", values=["value"])],
    ),
    (
      "http://example.com?key=value%20with%20escapes",
      [pb.QueryParam(key="key", values=["value%20with%20escapes"])],
    ),
  ],
)
def test_get_url_query_params(
  input_url: str, expected_output: list[pb.QueryParam]
):
  assert get_url_query_params(input_url) == expected_output


if __name__ == "__main__":
  raise SystemExit(pytest.main([__file__]))
