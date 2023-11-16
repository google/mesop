from optic.components import text, checkbox, button as button
import optic.state as state
import optic.state.decorator as decorator
from optic.store import store

text = text.text
checkbox = checkbox.checkbox


CheckboxEvent = state.CheckboxEvent
ClickEvent = state.ClickEvent
Key = state.Key

on = decorator.handler
store = store.store
