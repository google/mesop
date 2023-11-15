from optic.components import button, text, checkbox
import optic.state as state
import optic.state.decorator as decorator
from optic.store import store

button = button.button
text = text.text
checkbox = checkbox.checkbox


CheckboxEvent = state.CheckboxEvent
ClickEvent = state.ClickEvent
Key = state.Key

on = decorator.handler
store = store.store
