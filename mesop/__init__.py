from typing import Any, TypeVar, cast

from mesop.commands.navigate import navigate as navigate
from mesop.component_helpers import (
  Border as Border,
)
from mesop.component_helpers import (
  BorderSide as BorderSide,
)
from mesop.component_helpers import (
  Margin as Margin,
)
from mesop.component_helpers import (
  Padding as Padding,
)
from mesop.component_helpers import (
  Style as Style,
)
from mesop.component_helpers.helper import (
  component as component,
)
from mesop.component_helpers.helper import (
  composite as composite,
)
from mesop.component_helpers.helper import (
  slot as slot,
)
from mesop.components.audio.audio import audio as audio
from mesop.components.badge.badge import badge as badge

# REF(//scripts/scaffold_component.py):insert_component_import_export
from mesop.components.box.box import box as box
from mesop.components.button.button import (
  button as button,
)
from mesop.components.button.button import (
  content_button as content_button,
)
from mesop.components.checkbox.checkbox import (
  CheckboxChangeEvent as CheckboxChangeEvent,
)
from mesop.components.checkbox.checkbox import (
  CheckboxIndeterminateChangeEvent as CheckboxIndeterminateChangeEvent,
)
from mesop.components.checkbox.checkbox import (
  checkbox as checkbox,
)
from mesop.components.checkbox.checkbox import (
  content_checkbox as content_checkbox,
)
from mesop.components.divider.divider import divider as divider
from mesop.components.icon.icon import icon as icon
from mesop.components.image.image import image as image
from mesop.components.input.input import input as input
from mesop.components.input.input import native_textarea as native_textarea
from mesop.components.input.input import textarea as textarea
from mesop.components.markdown.markdown import markdown as markdown
from mesop.components.plot.plot import (
  plot as plot,
)
from mesop.components.progress_bar.progress_bar import (
  progress_bar as progress_bar,
)
from mesop.components.progress_spinner.progress_spinner import (
  progress_spinner as progress_spinner,
)
from mesop.components.radio.radio import (
  RadioChangeEvent as RadioChangeEvent,
)
from mesop.components.radio.radio import (
  RadioOption as RadioOption,
)
from mesop.components.radio.radio import (
  radio as radio,
)
from mesop.components.select.select import (
  SelectOption as SelectOption,
)
from mesop.components.select.select import (
  SelectSelectionChangeEvent as SelectSelectionChangeEvent,
)
from mesop.components.select.select import (
  select as select,
)
from mesop.components.sidenav.sidenav import sidenav as sidenav
from mesop.components.slide_toggle.slide_toggle import (
  SlideToggleChangeEvent as SlideToggleChangeEvent,
)
from mesop.components.slide_toggle.slide_toggle import (
  slide_toggle as slide_toggle,
)
from mesop.components.slider.slider import (
  SliderValueChangeEvent as SliderValueChangeEvent,
)
from mesop.components.slider.slider import (
  slider as slider,
)
from mesop.components.text.text import text as text
from mesop.components.tooltip.tooltip import tooltip as tooltip
from mesop.components.video.video import video as video
from mesop.dataclass_utils import dataclass_with_defaults
from mesop.events import (
  ClickEvent as ClickEvent,
)
from mesop.events import (
  InputEvent as InputEvent,
)
from mesop.features import page as page
from mesop.key import Key as Key
from mesop.runtime import runtime
from mesop.server.colab_run import colab_run as colab_run
from mesop.server.run import run as run

_T = TypeVar("_T")


def state(state: type[_T]) -> _T:
  return runtime().context().state(state)


def stateclass(cls: type[_T] | None, **kw_args: Any) -> type[_T]:
  """
  Similar as dataclass, but it also registers with Mesop runtime().
  """

  def wrapper(cls: type[_T]) -> type[_T]:
    dataclass_cls = dataclass_with_defaults(cls, **kw_args)
    runtime().register_state_class(dataclass_cls)
    return dataclass_cls

  if cls is None:
    # too difficult to properly type annotate
    anyWrapper = cast(Any, wrapper)
    # We're called with parens.
    return anyWrapper

  return wrapper(cls)
