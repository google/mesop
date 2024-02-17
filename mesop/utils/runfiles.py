from rules_python.python.runfiles import runfiles  # type: ignore


def get_runfile_location(identifier: str) -> str:
  """Use this wrapper to retrieve a runfile because this util is replaced in downstream sync."""

  # runfiles doesn't exist when running outside of bazel (e.g. pip install)
  if runfiles.Create() is None:  # type: ignore
    # TODO: make this less brittle and don't hard code "../", instead walk up
    # to the "mesop" directory.
    return "../" + identifier[len("mesop/mesop/") :]
  return runfiles.Create().Rlocation(identifier)  # type: ignore
