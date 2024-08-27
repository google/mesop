import mesop as me


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/text",
)
def text():
  me.text(text="Card Gallery", type="headline-4", style=me.Style(margin=me.Margin(bottom=16)))
  
  with me.box(style=me.Style(
    display="grid",
    grid_template_columns="repeat(auto-fit, minmax(250px, 1fr))",
    gap=16,
    padding=me.Padding.all(16),
    background=me.theme_var("surface"),
    border_radius=8,
    box_shadow="0 4px 6px rgba(0, 0, 0, 0.1)"
  )):
      for i in range(8):
          with me.box(style=me.Style(
              background="white",
              padding=me.Padding.all(16),
              border_radius=8,
              box_shadow="0 2px 4px rgba(0, 0, 0, 0.05)",
              display="flex",
              flex_direction="column",
              align_items="center",
              justify_content="center"
          )):
              me.text(text=f"Card {i+1}", type="subtitle-1", style=me.Style(
                  margin=me.Margin(bottom=8),
                  color=me.theme_var("primary"),
                  font_weight="bold"
              ))
              me.text(text="This is a description of the card content.", type="body-2", style=me.Style(
                  text_align="center",
                  color=me.theme_var("on-surface")
              ))
              me.button("Action", on_click=lambda e: print(f"Card {i+1} clicked"), type="flat", style=me.Style(margin=me.Margin(top=12)))
