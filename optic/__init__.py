from optic.components.button.button import button as button
from optic.components.checkbox.checkbox import checkbox as checkbox
from optic.components.text.text import text as text

import optic.state as state
import optic.state.decorator as decorator
from optic.store import store


CheckboxEvent = state.CheckboxEvent
ClickEvent = state.ClickEvent
Key = state.Key

on = decorator.handler
store = store.store
