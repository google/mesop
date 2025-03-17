import random
import time
from typing import Callable

import mesop as me

_TEMPERATURE_MIN = 0.0
_TEMPERATURE_MAX = 2.0
_TOKEN_LIMIT_MIN = 1
_TOKEN_LIMIT_MAX = 8192


@me.stateclass
class State:
  title: str = "LLM Playground"
  # Prompt / Response
  input: str
  response: str
  # Tab open/close
  prompt_tab: bool = True
  response_tab: bool = True
  # Model configs
  selected_model: str = "gemini-1.5"
  selected_region: str = "us-east4"
  temperature: float = 1.0
  temperature_for_input: float = 1.0
  token_limit: int = _TOKEN_LIMIT_MAX
  token_limit_for_input: int = _TOKEN_LIMIT_MAX
  stop_sequence: str = ""
  stop_sequences: list[str]
  # Modal
  modal_open: bool = False
  # Workaround for clearing inputs
  clear_prompt_count: int = 0
  clear_sequence_count: int = 0


def load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  on_load=load,
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://mesop-dev.github.io"]
  ),
  path="/llm_playground",
  title="LLM Playground",
)
def page():
  state = me.state(State)

  # Modal
  with modal(modal_open=state.modal_open):
    me.text("Get code", type="headline-5")
    if "gemini" in state.selected_model:
      me.text(
        "Use the following code in your application to request a model response."
      )
      with me.box(style=_STYLE_CODE_BOX):
        me.markdown(
          _GEMINI_CODE_TEXT.format(
            content=state.input.replace('"', '\\"'),
            model=state.selected_model,
            region=state.selected_region,
            stop_sequences=make_stop_sequence_str(state.stop_sequences),
            token_limit=state.token_limit,
            temperature=state.temperature,
          )
        )
    else:
      me.text(
        "You can use the following code to start integrating your current prompt and settings into your application."
      )
      with me.box(style=_STYLE_CODE_BOX):
        me.markdown(
          _GPT_CODE_TEXT.format(
            content=state.input.replace('"', '\\"').replace("\n", "\\n"),
            model=state.selected_model,
            stop_sequences=make_stop_sequence_str(state.stop_sequences),
            token_limit=state.token_limit,
            temperature=state.temperature,
          )
        )
    me.button(label="Close", type="raised", on_click=on_click_modal)

  # Main content
  with me.box(style=_STYLE_CONTAINER):
    # Main Header
    with me.box(style=_STYLE_MAIN_HEADER):
      with me.box(style=_STYLE_TITLE_BOX):
        me.text(
          state.title,
          type="headline-6",
          style=me.Style(line_height="24px", margin=me.Margin(bottom=0)),
        )

    # Toolbar Header
    with me.box(style=_STYLE_CONFIG_HEADER):
      icon_button(
        icon="code", tooltip="Code", label="CODE", on_click=on_click_show_code
      )

    # Main Content
    with me.box(style=_STYLE_MAIN_COLUMN):
      # Prompt Tab
      with tab_box(header="Prompt", key="prompt_tab"):
        me.textarea(
          label="Write your prompt here, insert media and then click Submit",
          # Workaround: update key to clear input.
          key=f"prompt-{state.clear_prompt_count}",
          on_input=on_prompt_input,
          style=_STYLE_INPUT_WIDTH,
        )
        me.button(label="Submit", type="flat", on_click=on_click_submit)
        me.button(label="Clear", on_click=on_click_clear)

      # Response Tab
      with tab_box(header="Response", key="response_tab"):
        if state.response:
          me.markdown(state.response)
        else:
          me.markdown(
            "The model will generate a response after you click Submit."
          )

    # LLM Config
    with me.box(style=_STYLE_CONFIG_COLUMN):
      me.select(
        options=[
          me.SelectOption(label="Gemini 1.5", value="gemini-1.5"),
          me.SelectOption(label="Chat-GPT Turbo", value="gpt-3.5-turbo"),
        ],
        label="Model",
        style=_STYLE_INPUT_WIDTH,
        on_selection_change=on_model_select,
        value=state.selected_model,
      )

      if "gemini" in state.selected_model:
        me.select(
          options=[
            me.SelectOption(label="us-central1 (Iowa)", value="us-central1"),
            me.SelectOption(
              label="us-east4 (North Virginia)", value="us-east4"
            ),
          ],
          label="Region",
          style=_STYLE_INPUT_WIDTH,
          on_selection_change=on_region_select,
          value=state.selected_region,
        )

      me.text("Temperature", style=_STYLE_SLIDER_LABEL)
      with me.box(style=_STYLE_SLIDER_INPUT_BOX):
        with me.box(style=_STYLE_SLIDER_WRAP):
          me.slider(
            min=_TEMPERATURE_MIN,
            max=_TEMPERATURE_MAX,
            step=0.1,
            style=_STYLE_SLIDER,
            on_value_change=on_slider_temperature,
            value=state.temperature,
          )
        me.input(
          style=_STYLE_SLIDER_INPUT,
          value=str(state.temperature_for_input),
          on_input=on_input_temperature,
        )

      me.text("Output Token Limit", style=_STYLE_SLIDER_LABEL)
      with me.box(style=_STYLE_SLIDER_INPUT_BOX):
        with me.box(style=_STYLE_SLIDER_WRAP):
          me.slider(
            min=_TOKEN_LIMIT_MIN,
            max=_TOKEN_LIMIT_MAX,
            style=_STYLE_SLIDER,
            on_value_change=on_slider_token_limit,
            value=state.token_limit,
          )
        me.input(
          style=_STYLE_SLIDER_INPUT,
          value=str(state.token_limit_for_input),
          on_input=on_input_token_limit,
        )

      with me.box(style=_STYLE_STOP_SEQUENCE_BOX):
        with me.box(style=_STYLE_STOP_SEQUENCE_WRAP):
          me.input(
            label="Add stop sequence",
            style=_STYLE_INPUT_WIDTH,
            on_input=on_stop_sequence_input,
            # Workaround: update key to clear input.
            key=f"input-sequence-{state.clear_sequence_count}",
          )
        with me.content_button(
          style=me.Style(margin=me.Margin(left=10)),
          on_click=on_click_add_stop_sequence,
        ):
          with me.tooltip(message="Add stop Sequence"):
            me.icon(icon="add_circle")

      # Stop sequence "chips"
      for index, sequence in enumerate(state.stop_sequences):
        me.button(
          key=f"sequence-{index}",
          label=sequence,
          on_click=on_click_remove_stop_sequence,
          type="raised",
          style=_STYLE_STOP_SEQUENCE_CHIP,
        )


# HELPER COMPONENTS


@me.component
def icon_button(*, icon: str, label: str, tooltip: str, on_click: Callable):
  """Icon button with text and tooltip."""
  with me.content_button(on_click=on_click):
    with me.tooltip(message=tooltip):
      with me.box(style=me.Style(display="flex")):
        me.icon(icon=icon)
        me.text(
          label, style=me.Style(line_height="24px", margin=me.Margin(left=5))
        )


@me.content_component
def tab_box(*, header: str, key: str):
  """Collapsible tab box"""
  state = me.state(State)
  tab_open = getattr(state, key)
  with me.box(style=me.Style(width="100%", margin=me.Margin(bottom=20))):
    # Tab Header
    with me.box(
      key=key,
      on_click=on_click_tab_header,
      style=me.Style(padding=_DEFAULT_PADDING, border=_DEFAULT_BORDER),
    ):
      with me.box(style=me.Style(display="flex")):
        me.icon(
          icon="keyboard_arrow_down" if tab_open else "keyboard_arrow_right"
        )
        me.text(
          header,
          style=me.Style(
            line_height="24px", margin=me.Margin(left=5), font_weight="bold"
          ),
        )
    # Tab Content
    with me.box(
      style=me.Style(
        padding=_DEFAULT_PADDING,
        border=_DEFAULT_BORDER,
        display="block" if tab_open else "none",
      )
    ):
      me.slot()


@me.content_component
def modal(modal_open: bool):
  """Basic modal box."""
  with me.box(style=_make_modal_background_style(modal_open)):
    with me.box(style=_STYLE_MODAL_CONTAINER):
      with me.box(style=_STYLE_MODAL_CONTENT):
        me.slot()


# EVENT HANDLERS


def on_click_clear(e: me.ClickEvent):
  """Click event for clearing prompt text."""
  state = me.state(State)
  state.clear_prompt_count += 1
  state.input = ""
  state.response = ""


def on_prompt_input(e: me.InputEvent):
  """Capture prompt input."""
  state = me.state(State)
  state.input = e.value


def on_model_select(e: me.SelectSelectionChangeEvent):
  """Event to select model."""
  state = me.state(State)
  state.selected_model = e.value


def on_region_select(e: me.SelectSelectionChangeEvent):
  """Event to select GCP region (Gemini models only)."""
  state = me.state(State)
  state.selected_region = e.value


def on_slider_temperature(e: me.SliderValueChangeEvent):
  """Event to adjust temperature slider value."""
  state = me.state(State)
  state.temperature = float(e.value)
  state.temperature_for_input = state.temperature


def on_input_temperature(e: me.InputEvent):
  """Event to adjust temperature slider value by input."""
  state = me.state(State)
  try:
    temperature = float(e.value)
    if _TEMPERATURE_MIN <= temperature <= _TEMPERATURE_MAX:
      state.temperature = temperature
  except ValueError:
    pass


def on_slider_token_limit(e: me.SliderValueChangeEvent):
  """Event to adjust token limit slider value."""
  state = me.state(State)
  state.token_limit = int(e.value)
  state.token_limit_for_input = state.token_limit


def on_input_token_limit(e: me.InputEvent):
  """Event to adjust token limit slider value by input."""
  state = me.state(State)
  try:
    token_limit = int(e.value)
    if _TOKEN_LIMIT_MIN <= token_limit <= _TOKEN_LIMIT_MAX:
      state.token_limit = token_limit
  except ValueError:
    pass


def on_stop_sequence_input(e: me.InputEvent):
  """Capture stop sequence input."""
  state = me.state(State)
  state.stop_sequence = e.value


def on_click_add_stop_sequence(e: me.ClickEvent):
  """Save stop sequence. Will create "chip" for the sequence in the input."""
  state = me.state(State)
  if state.stop_sequence:
    state.stop_sequences.append(state.stop_sequence)
    state.clear_sequence_count += 1


def on_click_remove_stop_sequence(e: me.ClickEvent):
  """Click event that removes the stop sequence that was clicked."""
  state = me.state(State)
  index = int(e.key.replace("sequence-", ""))
  del state.stop_sequences[index]


def on_click_tab_header(e: me.ClickEvent):
  """Open and closes tab content."""
  state = me.state(State)
  setattr(state, e.key, not getattr(state, e.key))


def on_click_show_code(e: me.ClickEvent):
  """Opens modal to show generated code for the given model configuration."""
  state = me.state(State)
  state.modal_open = True


def on_click_modal(e: me.ClickEvent):
  """Allows modal to be closed."""
  state = me.state(State)
  if state.modal_open:
    state.modal_open = False


def on_click_submit(e: me.ClickEvent):
  """Submits prompt to test model configuration.

  This example returns canned text. A real implementation
  would call APIs against the given configuration.
  """
  state = me.state(State)
  for line in transform(state.input):
    state.response += line
    yield


def transform(input: str):
  """Transform function that returns canned responses."""
  for line in random.sample(LINES, random.randint(3, len(LINES) - 1)):
    time.sleep(0.3)
    yield line + " "


LINES = [
  "Mesop is a Python-based UI framework designed to simplify web UI development for engineers without frontend experience.",
  "It leverages the power of the Angular web framework and Angular Material components, allowing rapid construction of web demos and internal tools.",
  "With Mesop, developers can enjoy a fast build-edit-refresh loop thanks to its hot reload feature, making UI tweaks and component integration seamless.",
  "Deployment is straightforward, utilizing standard HTTP technologies.",
  "Mesop's component library aims for comprehensive Angular Material component coverage, enhancing UI flexibility and composability.",
  "It supports custom components for specific use cases, ensuring developers can extend its capabilities to fit their unique requirements.",
  "Mesop's roadmap includes expanding its component library and simplifying the onboarding processs.",
]


# HELPERS

_GEMINI_CODE_TEXT = """
```python
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models

def generate():
  vertexai.init(project="<YOUR-PROJECT-ID>", location="{region}")
  model = GenerativeModel("{model}")
  responses = model.generate_content(
      [\"\"\"{content}\"\"\"],
      generation_config=generation_config,
      safety_settings=safety_settings,
      stream=True,
  )

  for response in responses:
    print(response.text, end="")


generation_config = {{
    "max_output_tokens": {token_limit},
    "stop_sequences": [{stop_sequences}],
    "temperature": {temperature},
    "top_p": 0.95,
}}

safety_settings = {{
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}}

generate()
```
""".strip()

_GPT_CODE_TEXT = """
```python
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="{model}",
  messages=[
    {{
      "role": "user",
      "content": "{content}"
    }}
  ],
  temperature={temperature},
  max_tokens={token_limit},
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0,
  stop=[{stop_sequences}]
)
```
""".strip()


def make_stop_sequence_str(stop_sequences: list[str]) -> str:
  """Formats stop sequences for code output (list of strings)."""
  return ",".join(map(lambda s: f'"{s}"', stop_sequences))


# STYLES


def _make_modal_background_style(modal_open: bool) -> me.Style:
  """Makes style for modal background.

  Args:
    modal_open: Whether the modal is open.
  """
  return me.Style(
    display="block" if modal_open else "none",
    position="fixed",
    z_index=1000,
    width="100%",
    height="100%",
    overflow_x="auto",
    overflow_y="auto",
    background="rgba(0,0,0,0.4)",
  )


_DEFAULT_PADDING = me.Padding.all(15)
_DEFAULT_BORDER = me.Border.all(
  me.BorderSide(color=me.theme_var("outline-variant"), width=1, style="solid")
)

_STYLE_INPUT_WIDTH = me.Style(width="100%")
_STYLE_SLIDER_INPUT_BOX = me.Style(display="flex", flex_wrap="wrap")
_STYLE_SLIDER_WRAP = me.Style(flex_grow=1)
_STYLE_SLIDER_LABEL = me.Style(padding=me.Padding(bottom=10))
_STYLE_SLIDER = me.Style(width="90%")
_STYLE_SLIDER_INPUT = me.Style(width=75)

_STYLE_STOP_SEQUENCE_BOX = me.Style(display="flex")
_STYLE_STOP_SEQUENCE_WRAP = me.Style(flex_grow=1)

_STYLE_CONTAINER = me.Style(
  display="grid",
  grid_template_columns="5fr 2fr",
  grid_template_rows="auto 5fr",
  height="100vh",
)

_STYLE_MAIN_HEADER = me.Style(
  border=_DEFAULT_BORDER, padding=me.Padding.all(15)
)

_STYLE_MAIN_COLUMN = me.Style(
  border=_DEFAULT_BORDER,
  padding=me.Padding.all(15),
  overflow_y="scroll",
)

_STYLE_CONFIG_COLUMN = me.Style(
  border=_DEFAULT_BORDER,
  padding=me.Padding.all(15),
  overflow_y="scroll",
)

_STYLE_TITLE_BOX = me.Style(display="inline-block")

_STYLE_CONFIG_HEADER = me.Style(
  border=_DEFAULT_BORDER, padding=me.Padding.all(10)
)

_STYLE_STOP_SEQUENCE_CHIP = me.Style(margin=me.Margin.all(3))

_STYLE_MODAL_CONTAINER = me.Style(
  background=me.theme_var("surface-container-high"),
  margin=me.Margin.symmetric(vertical="0", horizontal="auto"),
  width="min(1024px, 100%)",
  box_sizing="content-box",
  height="100vh",
  overflow_y="scroll",
  box_shadow=("0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f"),
)

_STYLE_MODAL_CONTENT = me.Style(margin=me.Margin.all(30))

_STYLE_CODE_BOX = me.Style(
  font_size=13,
  margin=me.Margin.symmetric(vertical=10, horizontal=0),
)
