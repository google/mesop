import mesop as me
from ai.common.prompt_context import prompt_context_store
from ai.console.scaffold import page_scaffold
from ai.offline_common.golden_dataset import create_golden_dataset


def on_load(e: me.LoadEvent):
  me.set_theme_mode("system")


def get_prompt_context_options():
  return [
    me.SelectOption(label=context.id, value=context.id)
    for context in prompt_context_store.get_all()
  ]


@me.stateclass
class State:
  prompt_context_id: str
  dataset_name: str
  dataset_path: str


def select_prompt_context(e: me.SelectSelectionChangeEvent):
  state = me.state(State)
  state.prompt_context_id = e.value


def on_dataset_name_blur(e: me.InputBlurEvent):
  state = me.state(State)
  state.dataset_name = e.value


@me.page(path="/create-golden-dataset", on_load=on_load)
def create_golden_dataset_page():
  state = me.state(State)
  with page_scaffold(
    current_path="/create-golden-dataset", title="Create golden dataset"
  ):
    me.input(
      label="Dataset name",
      on_blur=on_dataset_name_blur,
    )
    me.select(
      label="Prompt Context",
      options=get_prompt_context_options(),
      style=me.Style(width="min(100%, 360px)"),
      on_selection_change=select_prompt_context,
    )
    with me.box(
      style=me.Style(
        padding=me.Padding(bottom=16),
        display="flex",
        justify_content="space-between",
      )
    ):
      me.button(
        "Back",
        on_click=lambda e: me.navigate("/golden-examples"),
        type="stroked",
        color="accent",
      )
      me.button(
        "Create dataset",
        on_click=create_dataset,
        type="flat",
        color="accent",
      )
    if state.dataset_path:
      me.text(state.dataset_path)


def create_dataset(e: me.ClickEvent):
  state = me.state(State)
  prompt_context_id = state.prompt_context_id
  dataset_name = state.dataset_name
  prompt_context = prompt_context_store.get(prompt_context_id)
  dataset_path = create_golden_dataset(prompt_context, dataset_name)
  state.dataset_path = dataset_path
  print("dataset_path", dataset_path)
