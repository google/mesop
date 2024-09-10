import ai.console.scaffold as scaffold
import mesop as me


@me.page(title="Mesop AI Console", path="/")
def index_page():
  with scaffold.page_scaffold(current_path="/", title="Home"):
    me.markdown(
      """
# Welcome to the Mesop AI Console

Core concepts:

- **Producer**: A producer is a fully-configured LLM that can be used to generate responses for eval or live inference.
      """
    )
