import os


def get_path_from_workspace_root(*args: str) -> str:
  path_args = [_get_bazel_workspace_directory(), *list(args)]
  return os.path.join(*path_args)


def _get_bazel_workspace_directory() -> str:
  value = os.environ.get("BUILD_WORKSPACE_DIRECTORY")
  assert value
  return value
