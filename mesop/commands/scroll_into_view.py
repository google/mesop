from mesop.runtime import runtime


def scroll_into_view(*, key: str) -> None:
  """
  Scrolls so the component specified by the key is in the viewport.

  Args:
    key: The unique identifier of the component to scroll to.
               This key should be globally unique to prevent unexpected behavior.
               If multiple components share the same key, the first component
               instance found in the component tree will be scrolled to.
  """
  runtime().context().scroll_into_view(key)
