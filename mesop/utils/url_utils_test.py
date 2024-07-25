import pytest

from mesop.utils.url_utils import remove_url_query_param


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


if __name__ == "__main__":
  raise SystemExit(pytest.main([__file__]))
