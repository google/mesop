import builtins
import sys


def is_running_in_colab() -> bool:
  return "google.colab" in sys.modules and is_running_ipython()


def is_running_ipython():
  return hasattr(builtins, "get_ipython")
