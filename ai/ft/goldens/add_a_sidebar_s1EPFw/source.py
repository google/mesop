import mesop as me


@me.page(path="/ai")
def page():
  with me.box(
    style=me.Style(
      padding=me.Padding.all(24),
      background=me.theme_var("surface"),
      border_radius=8,
      box_shadow="0 2px 4px rgba(0, 0, 0, 0.1)",
    )
  ):
    me.text(
      "AI Page",
      type="headline-3",
      style=me.Style(
        margin=me.Margin(bottom=20), color=me.theme_var("primary")
      ),
    )
    me.text(
      "Welcome to the AI Page. Here you can explore various AI features.",
      type="body-1",
      style=me.Style(margin=me.Margin(bottom=30)),
    )

    # Add a button to explore AI features
    me.button(
      "Explore Features",
      on_click=explore_features,
      type="flat",
      style=me.Style(margin=me.Margin(bottom=20), align_self="start"),
    )

    # Add a grid layout for showcasing features
    with me.box(
      style=me.Style(
        display="grid", grid_template_columns="repeat(3, 1fr)", gap=16
      )
    ):
      for feature in AI_FEATURES:
        ai_feature_card(feature)


def explore_features(e: me.ClickEvent):
  # Logic to explore features
  pass


def ai_feature_card(feature: str):
  with me.box(
    style=me.Style(
      padding=me.Padding.all(16),
      background=me.theme_var("surface-variant"),
      border_radius=8,
      border=me.Border.all(
        me.BorderSide(width=1, color=me.theme_var("outline"))
      ),
      box_shadow="0 1px 2px rgba(0, 0, 0, 0.05)",
    )
  ):
    me.text(
      feature, type="subtitle-1", style=me.Style(margin=me.Margin(bottom=8))
    )
    me.text(
      "Description of the AI feature goes here.",
      type="body-2",
      style=me.Style(margin=me.Margin(bottom=12)),
    )
    me.button(
      "Learn More",
      on_click=lambda e: learn_more(feature),
      type="flat",
      style=me.Style(align_self="end"),
    )


def learn_more(feature: str):
  # Logic to learn more about a specific feature
  pass


AI_FEATURES = ["Feature 1", "Feature 2", "Feature 3"]
