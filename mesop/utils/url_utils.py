from urllib.parse import urlparse, urlunparse


def remove_url_query_param(url: str) -> str:
  """
  Remove query parameters from a URL.

  Args:
      url: The input URL.
  """
  parsed = urlparse(url)
  return urlunparse(parsed._replace(query=""))
