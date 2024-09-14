import mesop as me
from ai.common.prompt_fragment import prompt_fragment_store
from ai.console.scaffold import page_scaffold


def on_load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  title="Mesop AI Console - Prompt Fragments",
  path="/prompt-fragments",
  on_load=on_load,
)
def prompt_fragments_page():
  with page_scaffold(
    current_path="/prompt-fragments", title="Prompt Fragments"
  ):
    with me.box(style=me.Style(padding=me.Padding(bottom=16))):
      me.button(
        "Add Prompt Fragment",
        on_click=lambda e: me.navigate("/prompt-fragments/add"),
        type="flat",
        color="accent",
      )
    prompt_fragments = prompt_fragment_store.get_all()
    with me.box(
      style=me.Style(
        display="grid",
        grid_template_columns="1fr 1fr 1fr 48px",
        gap=16,
        align_items="center",
      )
    ):
      # Header
      me.text("ID", style=me.Style(font_weight="bold"))
      me.text("Contents", style=me.Style(font_weight="bold"))
      me.text("Role", style=me.Style(font_weight="bold"))
      with me.tooltip(message="Chain of Thought"):
        me.text("CoT", style=me.Style(font_weight="bold"))
      # Body
      for prompt_fragment in prompt_fragments:
        me.button(
          prompt_fragment.id,
          on_click=lambda e: me.navigate(
            "/prompt-fragments/edit", query_params={"id": e.key}
          ),
          key=prompt_fragment.id,
          style=me.Style(font_size=16),
        )
        if prompt_fragment.content_value:
          me.text("Value: " + prompt_fragment.content_value[:10])
        elif prompt_fragment.content_path:
          me.text("Path: " + prompt_fragment.content_path)

        me.text(prompt_fragment.role)
        me.text(str(prompt_fragment.chain_of_thought))
