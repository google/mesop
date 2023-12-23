# Use this file to import all examples
# This file needs to be in "mesop/" because it loads pages
# from examples and components so this is the lowest common ancestor
# which is needed for hot reloading to work properly.

# Use import alias so Ruff doesn't complain about unused imports
from mesop.examples import buttons as buttons
from mesop.examples import composite as composite
from mesop.examples import error as error
from mesop.examples import generator as generator
from mesop.examples import index as index
from mesop.examples import nested as nested
from mesop.examples import playground as playground
from mesop.examples import playground_critic as playground_critic
from mesop.examples import readme_app as readme_app

# Do not import error_state_missing_init_prop because it cause all examples to fail.
from mesop.examples import simple as simple
from mesop.examples.docs import counter as counter
from mesop.examples.docs import hello_world as hello_world
from mesop.examples.docs import loading as loading
from mesop.examples.docs import streaming as streaming
from mesop.examples.shared.navmenu import scaffold

import mesop.components.text.e2e as text_e2e
import mesop.components.box.e2e as box_e2e
import mesop.components.checkbox.e2e as checkbox_e2e
import mesop.components.markdown.e2e as markdown_e2e
import mesop.components.input.e2e as input_e2e
import mesop.components.tooltip.e2e as tooltip_e2e
import mesop.components.badge.e2e as badge_e2e
import mesop.components.divider.e2e as divider_e2e
import mesop.components.icon.e2e as icon_e2e
import mesop.components.progress_bar.e2e as progress_bar_e2e
import mesop.components.progress_spinner.e2e as progress_spinner_e2e
import mesop.components.slide_toggle.e2e as slide_toggle_e2e
import mesop.components.radio.e2e as radio_e2e
import mesop.components.select.e2e as select_e2e
import mesop.components.slider.e2e as slider_e2e
# REF(//scripts/scaffold_component.py):insert_component_e2e_import_export
