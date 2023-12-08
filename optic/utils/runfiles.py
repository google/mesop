from rules_python.python.runfiles import runfiles  # type: ignore


def get_runfile_location(identifier: str) -> str:
  """Use this wrapper to retrieve a runfile because this util is replaced in downstream sync."""
  return runfiles.Create().Rlocation(identifier)  # type: ignore
