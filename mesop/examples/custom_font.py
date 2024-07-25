import mesop as me


@me.page(
  path="/custom_font",
  stylesheets=[
    "https://fonts.googleapis.com/css2?family=Inter+Tight:ital,wght@0,100..900;1,100..900&family=Inter:wght@100..900&display=swap",
    "https://fonts.googleapis.com/css2?family=Tiny5&display=swap",
  ],
)
def app():
  me.text("Custom font: Inter Tight", style=me.Style(font_family="Inter Tight"))
  me.text("Custom font: Tiny5", style=me.Style(font_family="Tiny5"))
