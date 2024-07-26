from urllib.parse import urlparse, urlunparse

import mesop.protos.ui_pb2 as pb


def remove_url_query_param(url: str) -> str:
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
  return _escape_url_for_csp(remove_url_query_param(url))


def get_url_query_params(url: str) -> list[pb.QueryParam]:
  query_param = urlparse(url).query
  param_dict: dict[str, list[str]] = {}
  if query_param:
    for param in query_param.split("&"):
      if "=" in param:
        key, value = param.split("=", 1)
        if key in param_dict:
          param_dict[key].append(value)
        else:
          param_dict[key] = [value]
      else:
        # Handle cases where there's a key without a value
        param_dict[param] = []

  param_list: list[pb.QueryParam] = [
    pb.QueryParam(key=key, values=values) for key, values in param_dict.items()
  ]
  return param_list
