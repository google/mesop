from typing import Any
from optic.components import button, text, checkbox
import optic.state as state
import optic.state.decorator as decorator
import optic.lib.runtime as runtime

button = button.button
text = text.text
checkbox = checkbox.checkbox


CheckboxEvent = state.CheckboxEvent
ClickEvent = state.ClickEvent
on = decorator.handler


def store(state: Any):
    return runtime.runtime.session().create_store(state)
