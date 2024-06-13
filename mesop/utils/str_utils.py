import re


def snake_case(str: str) -> str:
  """
  Split UpperCamelCase and make it snake_case
  """
  return re.sub(r"(?<!^)(?=[A-Z])", "_", str).lower()
