import builtins
import sys


def is_running_in_colab() -> bool:
  return "google.colab" in sys.modules and hasattr(builtins, "get_ipython")
