import ai.console.scaffold as scaffold
import mesop as me
from ai.console.pages import add_edit_eval_page as add_edit_eval_page
from ai.console.pages import (
  add_edit_expected_examples_page as add_edit_expected_examples_page,
)
from ai.console.pages import (
  add_edit_golden_examples_page as add_edit_golden_examples_page,
)
from ai.console.pages import add_edit_model_page as add_edit_model_page
from ai.console.pages import add_edit_producer_page as add_edit_producer_page
from ai.console.pages import (
  add_edit_prompt_context_page as add_edit_prompt_context_page,
)
from ai.console.pages import (
  add_edit_prompt_fragment_page as add_edit_prompt_fragment_page,
)
from ai.console.pages import (
  create_golden_dataset_page as create_golden_dataset_page,
)
from ai.console.pages import eval_item_page as eval_item_page
from ai.console.pages import eval_page as eval_page
from ai.console.pages import evals_page as evals_page
from ai.console.pages import expected_examples_page as expected_examples_page
from ai.console.pages import golden_examples_page as golden_examples_page
from ai.console.pages import models_page as models_page
from ai.console.pages import producers_page as producers_page
from ai.console.pages import prompt_contexts_page as prompt_contexts_page
from ai.console.pages import prompt_fragments_page as prompt_fragments_page


def on_load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(title="Mesop AI Console", path="/", on_load=on_load)
def index_page():
  with scaffold.page_scaffold(current_path="/", title="Home"):
    me.markdown(
      """
# Mesop AI Console Overview

## Principles

- **Version Control**: Mesop AI Console is a UI on top of the [mesop-data](https://huggingface.co/datasets/wwwillchen/mesop-data) Git repo.
    - If you make changes, you should `cd ai/data` and commit the Git changes and push/make a pull request.

## Core Entities

- **Producer**: A producer fully specifies how to call a model, including configurations like temperature, prompt context, and how to process its outputs (e.g. taking the diff and apply it to the input code).
    - A producer can be used for inference (online) or evaluation (offline).
    - Producer = Model + Prompt Context + Settings (e.g. temperature, output format)

- **Prompt Context**: A prompt context is a prompt template with variables that are filled in at execution time.
    - A prompt context consists of one or more prompt fragments.

- **Prompt Fragment**: A prompt fragment is a chunk of a prompt for a specific role, e.g. `user` or `system`
    - Note: you can have multiple fragments with the same role, which are effectively concatenated together.

- **Example**: An example is a single input/output pair.
    - Examples are used for fine-tuning a model (i.e. golden example) or running an eval (i.e. expected example).
    - There are two types of examples:
        - **Golden Example**: A golden example is an example that is used to create a golden dataset.
        - **Expected Example**: An expected example is an example that is used to evaluate a producer.
        Internally, once an expected example has been run through an eval, we create an **evaluated example**, but you don't need to create this manually in the UI.
          """,
      style=me.Style(line_height=1.5),
    )
