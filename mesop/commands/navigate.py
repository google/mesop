from mesop.runtime import runtime


def navigate(url: str) -> None:
  runtime().context().navigate(url)
