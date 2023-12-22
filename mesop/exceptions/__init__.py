from .format_traceback import format_traceback as format_traceback


class MesopException(Exception):
  pass


class MesopUserException(Exception):
  def __str__(self):
    return f"**User Error:** {super().__str__()}"


class MesopInternalException(Exception):
  def __str__(self):
    return f"**Mesop Internal Error:** {super().__str__()}"


class MesopDeveloperException(Exception):
  def __str__(self):
    return f"**Mesop Developer Error:** {super().__str__()}"
