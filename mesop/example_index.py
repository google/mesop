# Use this file to import all examples
# This file needs to be in "mesop/" because it loads pages
# from examples and components so this is the lowest common ancestor
# which is needed for hot reloading to work properly.

# Use import alias so Ruff doesn't complain about unused imports
import mesop.examples as examples

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
import mesop.components.image.e2e as image_e2e
import mesop.components.audio.e2e as audio_e2e
import mesop.components.video.e2e as video_e2e
import mesop.components.sidenav.e2e as sidenav_e2e
import mesop.components.table.e2e as table_e2e
import mesop.components.embed.e2e as embed_e2e
import mesop.components.uploader.e2e as uploader_e2e
import mesop.components.html.e2e as html_e2e
import mesop.components.link.e2e as link_e2e
# REF(//scripts/scaffold_component.py):insert_component_e2e_import_export
