#########################
### COMPONENTS
#########################
from optic.components.button.button import button as button
from optic.components.checkbox.checkbox import checkbox as checkbox
from optic.components.text.text import text as text
# REF(//scripts/gen_component.py):insert_component_import_export

import optic.state as state
import optic.state.decorator as decorator
from optic.store import store
from optic.features import page as page


CheckboxEvent = state.CheckboxEvent
ClickEvent = state.ClickEvent
Key = state.Key

on = decorator.handler
store = store.store
