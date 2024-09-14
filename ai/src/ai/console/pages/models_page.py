import mesop as me
from ai.common.model import model_store as store
from ai.console.scaffold import page_scaffold


def on_load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(title="Mesop AI Console - Models", path="/models", on_load=on_load)
def models_page():
  with page_scaffold(current_path="/models", title="Models"):
    with me.box(style=me.Style(padding=me.Padding(bottom=16))):
      me.button(
        "Add Model",
        on_click=lambda e: me.navigate("/models/add"),
        type="flat",
        color="accent",
      )
    models = store.get_all()
    with me.box(
      style=me.Style(
        display="grid",
        grid_template_columns="repeat(3, 1fr)",
        gap=16,
        align_items="center",
      )
    ):
      # Header
      me.text("ID", style=me.Style(font_weight="bold"))
      me.text("Name", style=me.Style(font_weight="bold"))
      me.text("Provider", style=me.Style(font_weight="bold"))
      # Body
      for model in models:
        me.button(
          model.id,
          on_click=lambda e: me.navigate(
            "/models/edit", query_params={"id": e.key}
          ),
          key=model.id,
          style=me.Style(font_size=16),
        )
        me.text(model.name)
        me.text(model.provider)
