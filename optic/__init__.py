#########################
### COMPONENTS
#########################
from optic.components.button.button import button as button
from optic.components.checkbox.checkbox import checkbox as checkbox
from optic.components.text.text import text as text
from optic.components.box.box import box as box
# REF(//scripts/gen_component.py):insert_component_import_export

import optic.interactivity as interactivity
import optic.interactivity.decorator as decorator
from optic.store.store import store as store, state as export_state
from optic.features import page as page


CheckboxEvent = interactivity.CheckboxEvent
ClickEvent = interactivity.ClickEvent
Key = interactivity.Key

on = decorator.handler
interactivity = export_state
