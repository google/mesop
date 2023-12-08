from .format_traceback import format_traceback as format_traceback


class OpticException(Exception):
  pass


class OpticUserException(Exception):
  def __str__(self):
    return f"User Error: {super().__str__()}"


class OpticInternalException(Exception):
  pass


class OpticDeveloperException(Exception):
  pass
