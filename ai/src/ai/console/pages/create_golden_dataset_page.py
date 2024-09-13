import mesop as me
from ai.common.producer import producer_store
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
  producer_id: str
  dataset_name: str
  dataset_path: str


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
    me.autocomplete(
      label="Producer id",
      options=get_producer_ids(),
      style=me.Style(width="100%"),
      on_selection_change=select_producer_id,
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
      me.text("Created golden dataset at the following path:")
      me.text(state.dataset_path)


def select_producer_id(e: me.AutocompleteSelectionChangeEvent):
  state = me.state(State)
  state.producer_id = e.value


def create_dataset(e: me.ClickEvent):
  state = me.state(State)
  producer_id = state.producer_id
  dataset_name = state.dataset_name
  dataset_path = create_golden_dataset(
    producer_id=producer_id, dataset_name=dataset_name
  )
  state.dataset_path = dataset_path
  print("dataset_path", dataset_path)


def get_producer_ids():
  options: list[me.AutocompleteOption] = []

  for producer in producer_store.get_all():
    options.append(me.AutocompleteOption(label=producer.id, value=producer.id))

  return options
