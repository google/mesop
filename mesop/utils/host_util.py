import socket


def get_default_host() -> str:
  """
  This function returns the default host (which is externally accessible)
  based on the availability of IPv6.
  """
  if socket.has_ipv6:
    return "::"
  return "0.0.0.0"
