from mesop.runtime import runtime


def navigate(url: str) -> None:
  """
  Navigates to the given URL.

  Args:
    url: The URL to navigate to.
  """
  runtime().context().navigate(url)
