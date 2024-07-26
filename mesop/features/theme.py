from typing import Literal

import mesop.protos.ui_pb2 as pb
from mesop.runtime import runtime

ThemeMode = Literal["system", "light", "dark"]
ThemeBrightness = Literal["light", "dark"]


def set_theme_mode(theme_mode: ThemeMode) -> None:
  """
  Sets the theme mode for the application.

  Args:
      theme_mode: The desired theme mode. It can be "system", "light", or "dark".
  """
  if theme_mode == "dark":
    theme_mode_proto = pb.ThemeMode.THEME_MODE_DARK
  elif theme_mode == "light":
    theme_mode_proto = pb.ThemeMode.THEME_MODE_LIGHT
  else:
    theme_mode_proto = pb.ThemeMode.THEME_MODE_SYSTEM
  runtime().context().set_theme_mode(theme_mode_proto)


def theme_brightness() -> ThemeBrightness:
  """
  Returns the current theme brightness.

  This function checks the current theme being used by the application
  and returns whether it is "light" or "dark".
  """
  return "dark" if runtime().context().using_dark_theme() else "light"


ThemeVar = Literal[
  "background",
  "error",
  "error-container",
  "inverse-on-surface",
  "inverse-primary",
  "inverse-surface",
  "on-background",
  "on-error",
  "on-error-container",
  "on-primary",
  "on-primary-container",
  "on-primary-fixed",
  "on-primary-fixed-variant",
  "on-secondary",
  "on-secondary-container",
  "on-secondary-fixed",
  "on-secondary-fixed-variant",
  "on-surface",
  "on-surface-variant",
  "on-tertiary",
  "on-tertiary-container",
  "on-tertiary-fixed",
  "on-tertiary-fixed-variant",
  "outline",
  "outline-variant",
  "primary",
  "primary-container",
  "primary-fixed",
  "primary-fixed-dim",
  "scrim",
  "secondary",
  "secondary-container",
  "secondary-fixed",
  "secondary-fixed-dim",
  "shadow",
  "surface",
  "surface-bright",
  "surface-container",
  "surface-container-high",
  "surface-container-highest",
  "surface-container-low",
  "surface-container-lowest",
  "surface-dim",
  "surface-tint",
  "surface-variant",
  "tertiary",
  "tertiary-container",
  "tertiary-fixed",
  "tertiary-fixed-dim",
]


def theme_var(var: ThemeVar, /) -> str:
  """
  Returns the CSS variable for a given theme variable.

  Args:
      var: The theme variable name. See the [Material Design docs](https://m3.material.io/styles/color/static/baseline#690f18cd-d40f-4158-a358-4cfdb3a32768) for more information about the colors available.
  """
  return f"var(--sys-{var})"
