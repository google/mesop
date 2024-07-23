from enum import Enum

import mesop.protos.ui_pb2 as pb
from mesop.runtime import runtime


class ThemeMode(Enum):
  SYSTEM = "system"
  LIGHT = "light"
  DARK = "dark"


def set_theme_mode(theme_mode: ThemeMode) -> None:
  if theme_mode == ThemeMode.DARK:
    theme_mode_proto = pb.ThemeMode.THEME_MODE_DARK
  elif theme_mode == ThemeMode.LIGHT:
    theme_mode_proto = pb.ThemeMode.THEME_MODE_LIGHT
  else:
    theme_mode_proto = pb.ThemeMode.THEME_MODE_SYSTEM
  runtime().context().set_theme_mode(theme_mode_proto)


class ThemeBrightness(Enum):
  LIGHT = "light"
  DARK = "dark"


def theme_brightness() -> ThemeBrightness:
  return runtime().context().theme_brightness()
