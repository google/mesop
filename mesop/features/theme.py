from typing import Literal

import mesop.protos.ui_pb2 as pb
from mesop.runtime import runtime

ThemeMode = Literal["system", "light", "dark"]
ThemeBrightness = Literal["light", "dark"]


def set_theme_mode(theme_mode: ThemeMode) -> None:
  if theme_mode == "dark":
    theme_mode_proto = pb.ThemeMode.THEME_MODE_DARK
  elif theme_mode == "light":
    theme_mode_proto = pb.ThemeMode.THEME_MODE_LIGHT
  else:
    theme_mode_proto = pb.ThemeMode.THEME_MODE_SYSTEM
  runtime().context().set_theme_mode(theme_mode_proto)


def theme_brightness() -> ThemeBrightness:
  return "dark" if runtime().context().using_dark_theme() else "light"
