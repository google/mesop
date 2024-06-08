import os


def upper_camel_case(str: str) -> str:
  """
  Split underscore and make it UpperCamelCase
  """
  return "".join(x.title() for x in str.split("_"))


def wrap_quote(str: str) -> str:
  return f"'{str}'"


def snake_case(str: str) -> str:
  """
  Split UpperCamelCase and make it snake_case
  """
  snake_str = [str[0].lower()]
  for char in str[1:]:
    if char.isupper():
      snake_str.append("_")
    snake_str.append(char.lower())
  return "".join(snake_str)


def capitalize_first_letter(s: str) -> str:
  if not s:
    return s
  return s.capitalize()


def get_path_from_workspace_root(*args: str) -> str:
  path_args = [_get_bazel_workspace_directory()] + list(args)
  return os.path.join(*path_args)


def _get_bazel_workspace_directory() -> str:
  value = os.environ.get("BUILD_WORKSPACE_DIRECTORY")
  assert value
  return value
