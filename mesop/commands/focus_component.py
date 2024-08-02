from mesop.runtime import runtime


def focus_component(*, key: str) -> None:
  """
  Focus the component specified by the key

  Args:
    key: The unique identifier of the component to focus on.
               This key should be globally unique to prevent unexpected behavior.
               If multiple components share the same key, the first component
               instance found in the component tree will be focused on.
  """
  runtime().context().focus_component(key)
