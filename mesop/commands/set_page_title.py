from mesop.runtime import runtime


def set_page_title(title: str) -> None:
  """
  Sets the page title.

  Args:
    title: The new page title
  """
  runtime().context().set_page_title(title)
