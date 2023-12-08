from optic.api import state as state
from optic.api import stateclass as stateclass

# REF(//scripts/gen_component.py):insert_component_import_export
from optic.components.box.box import box as box
from optic.components.button.button import button as button
from optic.components.checkbox.checkbox import (
  CheckboxEvent as CheckboxEvent,
)
from optic.components.checkbox.checkbox import (
  checkbox as checkbox,
)
from optic.components.text.text import text as text
from optic.components.text_input.text_input import text_input as text_input
from optic.event_handler import event_handler
from optic.events import (
  ChangeEvent as ChangeEvent,
)
from optic.events import (
  ClickEvent as ClickEvent,
)
from optic.features import page as page
from optic.key import Key as Key

# Give a short alias for event handler since it's ubiquitous.
on = event_handler
