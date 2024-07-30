from urllib.parse import urlparse, urlunparse


def _remove_url_query_param(url: str) -> str:
  """
  Remove query parameters from a URL.

  Args:
      url: The input URL.
  """
  parsed = urlparse(url)
  return urlunparse(parsed._replace(query=""))


def _escape_url_for_csp(url: str) -> str:
  escaped_url = url.replace(";", "%3B").replace(",", "%2C")
  return escaped_url


def sanitize_url_for_csp(url: str) -> str:
  return _escape_url_for_csp(_remove_url_query_param(url))
