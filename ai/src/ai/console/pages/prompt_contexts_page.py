import mesop as me
from ai.common.prompt_context import prompt_context_store
from ai.console.scaffold import page_scaffold


def on_load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  title="Mesop AI Console - Prompt Contexts",
  path="/prompt-contexts",
  on_load=on_load,
)
def prompt_contexts_page():
  with page_scaffold(current_path="/prompt-contexts", title="Prompt Contexts"):
    prompt_contexts = prompt_context_store.get_all()
    with me.box(style=me.Style(padding=me.Padding(bottom=16))):
      me.button(
        "Add Prompt Context",
        on_click=lambda e: me.navigate("/prompt-contexts/add"),
        type="flat",
        color="accent",
      )
    with me.box(
      style=me.Style(
        display="grid",
        grid_template_columns="400px 400px",
        gap=16,
        align_items="center",
      )
    ):
      # Header
      me.text("ID", style=me.Style(font_weight="bold"))
      me.text("Fragments", style=me.Style(font_weight="bold"))
      # Body
      for prompt_context in prompt_contexts:
        me.button(
          prompt_context.id,
          on_click=lambda e: me.navigate(
            "/prompt-contexts/edit", query_params={"id": e.key}
          ),
          key=prompt_context.id,
          style=me.Style(font_size=16, flex_wrap="wrap", word_wrap="anywhere"),
        )
        with me.box(style=me.Style(display="flex-wrap", flex_direction="row")):
          for fragment_id in prompt_context.fragment_ids:
            me.button(
              fragment_id,
              on_click=lambda e: me.navigate(
                "/prompt-fragments/edit", query_params={"id": e.key}
              ),
              key=fragment_id,
              style=me.Style(font_size=16),
            )
