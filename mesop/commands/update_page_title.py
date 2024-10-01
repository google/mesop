from mesop.runtime import runtime


def update_page_title(title: str) -> None:
  """
  Update the page title.

  Args:
    title: The updated page title
  """
  runtime().context().update_page_title(title)
