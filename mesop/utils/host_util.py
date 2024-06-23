import socket


def get_default_host() -> str:
  """
  Returns the default host (which is externally accessible)
  based on the availability of IPv6.
  """
  if has_ipv6():
    return "::"
  return "0.0.0.0"


# Context: https://github.com/urllib3/urllib3/pull/611
def has_ipv6():
  """Returns True if the system can bind an IPv6 address."""
  # First, check if Python was compiled with IPv6 support
  if not socket.has_ipv6:
    return False

  sock = None
  try:
    # Attempt to create an IPv6 socket
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

    # Try to bind to the IPv6 unspecified address
    # Note: cannot use IPv6 loopback address: "::1"
    # because it doesn't work on Colab, likely due to
    # some networking configuration w/ the container.
    #
    # Using port 0 lets the OS choose an available port
    sock.bind(("::", 0))

    # If we get here, the bind was successful
    return True
  except Exception:
    # An exception means IPv6 is not supported or cannot be used
    return False
  finally:
    # Ensure the socket is closed, even if an exception occurred
    if sock:
      sock.close()
